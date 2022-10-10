import sys
from utils.prettyprints import PRR, Colors

crm = {
    "clients": {
        "global": "Clients have contracts, each contract has"
                  " 0 or 1 event it is associated with.",
        "add": "Only members of the sales group can create new clients.",
        "change": "Only admins and the client's sales contact"
                  " can change a client.",
        "detail": "Only admins, client's sales contact and"
                  " support contacts of the client's events.",
        "list": "Except admins who see all clients, support and"
                " sales only see clients they are contact of.",
        "search": "Same as list, literal fields all support 'icontains',"
                  " numeric all support 'lt' and 'gt'.",
        "delete": "Only superuser can delete items."
    },
    "contracts": {
        "global": "Contracts can have 1 only event, if so their 'status'"
                  " is set to 'True' otherwise 'False.",
        "add": "Only members of the sales group can create new contracts"
               " for their clients.",
        "change": "Only admins and the client's sales contact can"
                  " change a contract.",
        "detail": "Only admins and client's sales contact.",
        "list": "Except admins who see all contracts, sales only see"
                " contract of clients they are contact of.",
        "search": "Same as list, literal fields all support 'icontains',"
                  " numeric all support 'lt' and 'gt'.",
        "delete": "Only superuser can delete items."
    },
    "events": {
        "global": "Events are related to a single contract via"
                  " the 'Status' model and to a client.",
        "add": "Only members of the sales group can "
               "create an event for their clients.",
        "change": "Only admins and the event's support contact can"
                  " change an event.",
        "detail": "Only admins, client's sales contact"
                  " and support contacts of the client / event.",
        "list": "Except admins who see all clients, "
                "support and sales only see clients they are contact of.",
        "search": "Same as list, literal fields all support 'icontains'"
                  ", numeric all support 'lt' and 'gt'.",
        "delete": "Only superuser can delete items."
    }
}

authentication = {
    "users": {
        "global": "Users can only be created/edited/viewed by admins"
                  " on the django admin site.\n"
                  " User have a 'role' that can be either"
                  " 'visitor', 'sales', 'support', 'admin'."
                  " User's roles are in fact associated with a group"
                  " of the same name.\n Changing the role will change both"
                  " the group and the permissions.",
        "delete": "Items in the crm are protected so you can not delete a user"
                  " if he is contact of an item."
                  " You can change the contact of client/clients "
                  "on the admin site with a crm/client action."
                  " This will also set the new contact for"
                  " all the clients contracts.\n"
                  " The same action exists to change the contact of event/events, next to the delete action."
    },
    "groups": {
        'global': "Admins should not have to deal with groups"
                  " and should change the role of the user instead",
        'visitor': "Visitors have no access at all.",
        'sales': "Members of Sales have add, change, view permission"
                 " for clients and contracts, create and view for events. "
                 "But also need to be contact of the client",
        'support': "Support members have view permission of the client, of "
                   "their events and change/view permission for their events",
        'admin': "Admins have access to the admin site and add/change/view"
                 " of all items in db"
    }
}

help_dict = {
    'global': "You can print a partial doc thanks to "
              "command line arguments to filter.\n"
              "You can print only the 'crm' or 'authentication' doc"
              " by adding these names as argument.\n"
              "Or any of the following models: 'client', 'contract',"
              " 'event', 'user', 'groups'."
              "You can also filter by action: \n"
              ' "add", "change", "detail", "list", "search", '
              '"delete", "sales", "support", "admin", "visitor"'
}


class Doc:
    doc = {"crm": crm,
           "authentication": authentication,
           "help": help_dict}
    apps = ["authentication", "crm"]
    models = ["clients", "contracts", "events", "groups", "users"]
    actions = ["add", "change", "detail", "list", "search", "delete",
               "sales", "support", "admin", "visitor"]

    def __init__(self, args):
        self.selected_apps = []
        self.selected_models = []
        self.selected_actions = []
        self.is_help = False
        for arg in args:
            if arg in self.actions:
                self.selected_actions.append(arg)
                if arg in self.actions[:6]:
                    self.selected_apps.append(self.apps[1])
                if arg in self.actions[5:]:
                    self.selected_apps.append(self.apps[0])

            for model in self.models:
                if arg in model:
                    self.selected_models.append(model)
                    if model in self.models[:3]:
                        self.selected_apps.append(self.apps[1])
                    else:
                        self.selected_apps.append(self.apps[0])
                    break
            if arg in self.apps:
                self.selected_apps.append(arg)
            if "help" in arg:
                self.is_help = True
        if not self.selected_apps:
            self.selected_apps = self.apps
        if not self.selected_actions:
            self.selected_actions = self.actions
        if not self.selected_models:
            self.selected_models = self.models

    def print(self):
        if self.is_help:
            print(f'{Colors.get("METHOD", "Help")}: {help_dict["global"]}')
        else:
            for app in set(self.selected_apps):
                print(f"\n{Colors.get('METHOD', app.upper())}:")
                for model in sorted(list(set(self.selected_models))):
                    title = Colors.get('URL', model.upper())
                    try:
                        msg = self.doc[app][model]['global']
                        print(f"\n  {title}:  {msg}")
                    except KeyError:
                        pass
                    for action in sorted(list(set(self.selected_actions))):
                        title = Colors.get('OK', action.upper())
                        try:
                            msg = self.doc[app][model][action]
                            print(f"\n    {title}: {msg}")
                        except KeyError:
                            pass
                        try:
                            PRR.print_doc(action, model, app)
                        except FileNotFoundError:
                            pass


if __name__ == "__main__":
    sys_args = [arg.lower() for arg in sys.argv]
    doc = Doc(sys_args)
    doc.print()
