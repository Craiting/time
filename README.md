# Quick reference #

## First Step, Getting dependencies ##

* After setting up your environment run: 'pip install -r requirments.txt' to get all dependencies

## Getting django-admin to run properly ##

* Edit the activate script of the virtualenv in the /bin folder (cd to virtual env folder - look below for command if you're using virtualenvwrapper)
* Add these two lines to the bottom:
```
export PYTHONPATH='PATH/TO/AETAS/PROJECT/aetas'
export DJANGO_SETTINGS_MODULE=settings
```
* The activate script is the same one to start your virtualenv

## django commands ##
Run server: `django-admin runserver`

Run migrations: `django-admin migrate`

All commands: `django-admin --help`

## virtualenvwrapper commands ##
Start project:
```
workon virtualenvwrapper
```

List all virtual envs:
```
lsvirtualenv
```

cd to virtual env (this isn't where the project files are!):
```
cdvirtualenv
```

deactivate virtualenv
```
deactivate
```