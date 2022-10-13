The simplest way to test it is to:

1. Postgres Credentials can be found/set in the config.py file in the epicevents folder:

The app need to connect to a Postgres database. You can either create a Postgres account with the username and
password in config.py or edit POSTGRES_USER, POSTGRES_PASSWORD in config.py to enter your account username and password.
      
2. Clone the repository on your own computer et navigate into the folder:

        git clone https://github.com/XDevant/P10_devant_xavier.git as P10
        cd P10

3. Create a new virtual environment in the root folder (the one this file):

        python -m venv env

4. Activate the virtual environment:
    + unix: source env/bin/activate
    + windows: env/Scripts/activate.ps1

5. Install the dependencies via the requirement.txt file:

        pip install -r requirements.txt

6. Install the app:

        python epicevents\manage.py install -sf
This will chain the makemigration and migrate commands, create groups and permissions,
and generate a group of fake users and items to test the app.
This will also create a database Epic-Events and duplicate it for use as testing template.
The flag -s ensures the creation of a superuser, needed for admin testing.
The flag -f loads the fake items in both db instead of only template db.


## The "install" command will try to create a Epic-Events database so make sure it doest not already exists
## or change the name in config.py (POSTGRES_NAME)
## It will also DROP the tables named dev_{POSTGRES_NAME}, test_{POSTGRES_NAME} and copy_{POSTGRES_NAME} before recreating them.


7. Run the selenium test server:

        cd epicevents
        python manage.py runseleniumserver
This will start a test server needed for selenium tests. It should run on Port 7000 instead of 8000
This will avoid selenium messing with the dev database in case of failure.

9. Test the app:

        pytest epicevents\apptest -vv -s
All tests using the database run on a copy of the database that was created during the installation named copy_Epic-Events.
Whatever happens to the default database after the install will have no effet on the tests.
But all tests need the fake users and fake_items to be loaded at install and selenium requires a superuser.

11. Admin url: http://127.0.0.1:8000/admin (runserver) or http://127.0.0.1:7000/admin (runseleniumserver)
Important: the database used by runseleniumserver is temporary and reinitialized every time the server it restarted.

Notes:

User logs can be found in the epicevents\authentication\fixtures\fake_users.py file


