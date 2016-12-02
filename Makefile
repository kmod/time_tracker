RUN_DEPS := dev_env #timetracker/db_timestamp
run: $(RUN_DEPS)
	dev_env/bin/python timetracker/manage.py runserver

shell: $(RUN_DEPS)
	dev_env/bin/python timetracker/manage.py shell
makemigrate makemigration makemigrations: $(RUN_DEPS)
	dev_env/bin/python timetracker/manage.py makemigrations tt
migrate: $(RUN_DEPS)
	dev_env/bin/python timetracker/manage.py migrate
superuser adminuser admin_user user: $(RUN_DEPS)
	dev_env/bin/python timetracker/manage.py createsuperuser

dev_env/timestamp: requirements.txt
	virtualenv dev_env -p python3
	dev_env/bin/pip install -r requirements.txt
	touch dev_env/timestamp
dev_env: dev_env/timestamp
