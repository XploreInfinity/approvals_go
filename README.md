<h1>Approvals GO!(Formerly Classroom GO!)</h1>
<i>Approvals Go allows you to quickly validate/approve internal PDF documents within your organisation.</i>

<h3>Features:</h3>

* Quick to setup
* Simple and minimalistic:There are two types of users: HODs and Faculties. Faculties submit PDF docs and HODs review them.
* Submitted documents can be approved,sent back for changes(with comments) or rejected.
* Once approved, documents become immutable.
* Robust user accounts system and security[powered,mostly by Django's inbuilt features], with password and username recovery options

<h3>Deployment:</h3>

Before deployment,do the following:

* Install Django and django-crispy-forms: run the following in your terminal/command-prompt: `pip install Django django-crispy-forms`
* Add a security key for the app: From the main project directory, go to `classroom_go/settings.py`.Find this line: `SECRET_KEY = ""#*add your own key here please :)`, then put a confidential and sufficiently long cryptic string between the double quotes.

* Add configuration for the email account that will provide the username/password recovery service: From the main project directory, go to `classroom_go/settings.py` and fill out the empty variables below this line: `EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'`

<h3>Running:</h3>

* In the main project directory, open a terminal/command-prompt and run this: `python manage.py runserver`
* The server should be ready at `http://localhost:8000`
* To kill the server: `Ctrl+C`
* NOTE: The above procedure uses Django's built in development server to run the app. In production, you should use a dedicated server like Apache instead.

<h3>[IMPORTANT]User Accounts and Initial Setup:</h3>

* To manage user accounts, go to `http://localhost:8000/admin`. All administrative actions like these use Django's admin dash.
* An administrator user is already setup for initial use, but it is strongly recommended to change the credentials of this user upon first login. For the first login, use these credentials: Username-> `SuperInsecure`; Password-> `Insecure_Password01`
* After the admin account is secured, you can create normal user accounts via the admin dash.
* Each normal user needs to be assigned a user group(either HOD or faculty,depending upon their role). A user not belonging to either of the groups will be denied access to the main application.

**This is Stable build v1.0. This project is past its active development(feel free to suggest new features, but I can't guarantee they will be implemented),however any new bugs reports will be addressed(open an issue).**

**Xploreinfinity ≧◠‿◠≦✌**