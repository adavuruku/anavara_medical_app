# anavara_medical_app
A medical app design for Anavara backend technical assessment role.

# **How to set up the project**
* first clone the project [Here](https://pages.github.com/)
* create a virtual env in the root folder using  python -m venv env
* activate the virtual env using env\bin\activate   
* install the requirement libraries python install -r requirements.txt

# **How to set up the project database**
* create a .env file in anavara/anavara and add the bellow ENVIRONMENT VARIABLES
```
    EMAIL_HOST_PASSWORD
    EMAIL_HOST_USER
    FRONTEND_URL
    SIGNING_KEY
    CORS_ALLOWED_ORIGINS
    DATABASE_URL 
```
* Any relational database of choise can be use [sqlite, postgress, mysql]
```
    the necessary changes should be made in DATABASES section of app setting anavara/anavara/settings.py

    for sqlite

    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    

    for postgres
    
    DATABASES = {
    'default': env.db('DATABASE_URL',
                      'postgres://postgres:root@127.0.0.1:5432/anavara',
                    'django.contrib.gis.db.backends.postgis'),
}
```
* from the terminal on the activate virtual environment console, create 
    - create migration using python manage.py makemigrations
    - apply the migration using python manage.py migrate
    - you can create a superuser using python manage.py createsuperuser

# **API Documentation**

* start the project using python manage.py runserver <portnumer>
* add the base url example http://127.0.0.1:8080 to the env value CORS_ALLOWED_ORIGINS 8080 should be replaced with the port number you have used to start the project
* API (Swagger documentation) can be found in http://127.0.0.1:<port number>/swagger/ 
``` for example http://127.0.0.1:8081/swagger/ where 8081 will be replace with the port number you have started the poroject```

# **Project Design**

* **User** 
```
Users are the operator of the system that are responsible for providing data input to the system.
the different users of the system are super users, doctors, and staff.
Each of this user have role, access permission and the operation they can carried out in the system.
```
* Super User
``` A super user can carry out all operation available in the system and view, edit and create any record in the system ```

* Doctor User
``` A doctor user can create a patient record. Doctor can also create, view, edit and delete patient medical record of which they created  ```

* Staff User
``` A staff user have the minimal access as they can only create patient records ```
* Other Operation

``` Users can change or update their password by providing their previous and new password ```
``` Users can request to reset their password by providing their email id which will then be used to validate the account and forward an email with a reset account link to change or update their the password```

* **Patient Record** 
```
Patient record is the first entry point for every patient registered at the hospital, is at this point patients get their hospital id, which will then be use to track every of their activities at the hospital.
It has a relationship to user object through create_by foreign key [many to one]. this is to track the user that create/register the patients.
```

* **Medical Record** 
```
Medical record have the detail of every medical consultation report for every patients.
this is where user with doctor or super user access create a medical result for a patients,
It has a relationship to user object through doctor foreign key [many to one] and a relationship to patient object through patient field foreign key [many to one]. Doctor field is to tracek the doctor or super user that create the patient medical record while the patient foreign key is to track the patient that owns the medical record.

Only doctor and supper user can update and view this records.
Also, doctor can only view and update records they created
Super users can edit and update all record.
```
