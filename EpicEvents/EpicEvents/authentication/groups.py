
def create_groups(apps, schema_migration):
    """Used in authentication.migrations.0003_auto... to create our 2 user groups"""
    User = apps.get_model('authentication', 'User')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    class ModelPermissions:
        def __init__(self, model_name):
            self.add = Permission.objects.get(codename=f'add_{model_name}')
            self.change = Permission.objects.get(codename=f'change_{model_name}')
            self.delete = Permission.objects.get(codename=f'delete_{model_name}')
            self.view = Permission.objects.get(codename=f'view_{model_name}')
            self.permissions = [self.add, self.change, self.delete, self.view]

    contract_permissions = ModelPermissions('contract')
    client_permissions = ModelPermissions('client')
    event_permissions = ModelPermissions('event')

    support = Group(name='support')
    support.save()
    support.permissions.set(event_permissions.permissions)
    support.permissions.add(contract_permissions.view)
    support.permissions.add(client_permissions.view)

    sales = Group(name='sales')
    sales.save()
    support.permissions.set(
                            client_permissions.permissions +
                            contract_permissions.permissions +
                            event_permissions.permissions
                            )

    for user in User.objects.all():
        if user.role == 'support':
            user.groups.add(support)
        if user.role == 'sales':
            user.groups.add(sales)


"""
add this to migration.0002 list
        migrations.RunPython(create_groups)
"""
