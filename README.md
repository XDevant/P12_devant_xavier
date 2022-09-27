The simplest way to test it is to:

1. Postgres Credentials can be found/set in the config.py file in the epicevents folder:

The app need to connect to a Postgres database. You can either create a Postgres account with the name and
password in config.py or edit the config.py to enter your account name and password.
      
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

        python EpicEvents\manage.py install -sf
This will chain the makemigration and migrate commands, create groups and permissions,
and generate a group of fake users and items to test the app.
This will also create a database Epic-Events and duplicate it for use as testing template.
The flag -s ensures the creation of a superuser, needed for admin testing.
The flag -f loads the fake items in both db instead of only template db.

7. Run the server:

        cd epicevents
        python manage.py runserver

8. Test the app:

        pytest -vv -s

9. Admin url: http://127.0.0.1:8000/admin

Notes:

User logs can be found in the epicevents\authentication\fixtures\fake_users.py file


