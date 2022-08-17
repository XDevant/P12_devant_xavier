
def create_groups(apps, schema_migration):
    """Used in authentication.migrations.0002_auto... to create our user groups"""
    User = apps.get_model('authentication', 'User')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    class ModelPermissions:
        def __init__(self, model_name):
            self.add = Permission.objects.get(codename=f'add_{model_name}')
            self.change = Permission.objects.get(codename=f'change_{model_name}')
            self.delete = Permission.objects.get(codename=f'delete_{model_name}')
            self.view = Permission.objects.get(codename=f'view_{model_name}')
            self.permissions = [self.add, self.view, self.change, self.delete]

    contract_permissions = ModelPermissions('contract')
    client_permissions = ModelPermissions('client')
    event_permissions = ModelPermissions('event')
    user_permissions = ModelPermissions('user')

    support = Group(name='support')
    support.save()
    support.permissions.set(event_permissions.permissions[1:3])
    support.permissions.add(contract_permissions.view)
    support.permissions.add(client_permissions.view)

    sales = Group(name='sales')
    sales.save()
    support.permissions.set(client_permissions.permissions[:3] +
                            contract_permissions.permissions[:3] +
                            event_permissions.permissions[:2])
    support.permissions.add(event_permissions.view)
    support.permissions.add(event_permissions.add)

    visitor = Group(name='visitor')
    visitor.save()

    admin = Group(name='admin')
    admin.save()
    support.permissions.set(client_permissions.permissions[1:3] +
                            contract_permissions.permissions[1:3] +
                            event_permissions.permissions[1:3] +
                            user_permissions.permissions)

    for user in User.objects.all():
        if user.role == 'support':
            user.groups.add(support)
        elif user.role == 'sales':
            user.groups.add(sales)
        elif user.role == 'admin':
            user.groups.add(admin)
        else:
            if not user.is_superuser:
                user.groups.add('visitor')
