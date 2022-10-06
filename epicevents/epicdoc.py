import sys
from utils.prettyprints import PRR, Colors

crm = {
    "clients": {
        "global": "Clients have contracts, each contract has 0 or 1 event it is associated with.",
        "add": "Only members of the sales group can create new clients.",
        "change": "Only admins and the client's sales contact can change a client.",
        "detail": "Only admins, client's sales contact and support contacts of the client's events.",
        "list": "Except admins who see all clients, support and sales only see clients they are contact of.",
        "search": "Same as list, literal fields all support 'icontains', numeric all support 'lt' and 'gt'.",
        "delete": "Only superuser can delete items."
    },
    "contracts": {
        "global": "Contracts can have 1 only event, if so their 'status' is set to 'True' otherwise 'False.",
        "add": "Only members of the sales group can create new contracts for their clients.",
        "change": "Only admins and the client's sales contact can change a contract.",
        "detail": "Only admins and client's sales contact.",
        "list": "Except admins who see all contracts, sales only see contract of clients they are contact of.",
        "search": "Same as list, literal fields all support 'icontains', numeric all support 'lt' and 'gt'.",
        "delete": "Only superuser can delete items."
    },
    "events": {
        "global": "Events are related to a single contract via the 'Status' model and to a client.",
        "add": "Only members of the sales group can create an event for their clients.",
        "change": "Only admins and the event's support contact can change an event.",
        "detail": "Only admins, client's sales contact and support contacts of the client / event.",
        "list": "Except admins who see all clients, support and sales only see clients they are contact of.",
        "search": "Same as list, literal fields all support 'icontains', numeric all support 'lt' and 'gt'.",
        "delete": "Only superuser can delete items."
    }
}

authentication = {
    "users": {
        "global": "Users can only be created/edited/viewed by admins on the django admin site.\n"
                  + " User have a 'role' that can be either 'visitor', 'sales', 'support', 'admin'."
                  + " User's roles are in fact associated with a group of the same name.\n Changing"
                  + " the role will change the group and the permissions.",
        "delete": "Items in the crm are protected so you can not delete a user if he is contact of an item."
                  + " You can change the contact of client/clients on the admin site with a crm/client action."
                  + " This will also set the new contact for all the clients contracts.\n"
                  + " The same action exists to change the contact of event/events, next to the delete action."
    },
    "groups": {
        'global': "Admins should not have to deal with groups and should change the role of the user instead",
        'visitor': "Visitors have no access at all.",
        'sales': "Members of Sales have add, change, view permission for clients and contracts,"
                 " create and view for events. But also need to be contact of the client",
        'support': "Support members have view permission of the client of their events and change/view"
                   "permission for their events",
        'admin': "Admins have access to the admin site and add/change/view of all items in db"
    }
}

help_dict = {
    'global': "You can print a partial doc thanks to command line arguments to filter.\n"
              "You can print only the 'crm' or 'authentication' doc by adding these names as argument.\n"
              "Or any of the following models: 'client', 'contract', 'event', 'user', 'groups'."
              "You can also filter by action: \n"
              ' "add", "change", "detail", "list", "search", "delete", "sales", "support", "admin", "visitor"'
}

doc = {
    "crm": crm,
    "authentication": authentication,
    "help": help_dict
}

if __name__ == "__main__":
    apps = ["authentication", "crm"]
    models = ["clients", "contracts", "events", "groups", "users"]
    actions = ["add", "change", "detail", "list", "search", "delete", "sales", "support", "admin", "visitor"]
    is_help = False
    for arg in sys.argv:
        arg = arg.lower()
        if arg == "authentication":
            apps = ["authentication"]
            models = ["users", "groups"]
        if arg == "crm":
            apps = ["crm"]
            models = ["clients", "contracts", "events"]

        for model in ["client", "contract", "event"]:
            if model in arg:
                apps = ["crm"]
                models = [model + 's']
        for model in ["user", "groups"]:
            if model in arg:
                apps = ["authentication"]
                models = [model + 's']
        for action in ["add", "change", "detail", "list", "search"]:
            if arg == action:
                actions = [action]
        if "help" in arg.lower():
            is_help = True

    if is_help:
        print(f'{Colors.get("METHOD", "Help")}: {help_dict["global"]}')
    else:
        for app in apps:
            print(f"{Colors.get('METHOD', app.upper())}:")
            for model in models:
                try:
                    print(f"  {Colors.get('URL', model.upper())}:  {doc[app][model]['global']}")
                except KeyError:
                    pass
                for action in actions:
                    try:
                        print(f"    {Colors.get('OK', action.upper())}: {doc[app][model][action]}")
                    except KeyError:
                        pass
                    try:
                        PRR.print_doc(action, app, model)
                    except FileNotFoundError as e:
                        pass
