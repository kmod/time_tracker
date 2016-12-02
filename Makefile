dev_env/timestamp: requirements.txt
	virtualenv dev_env -p python3
	dev_env/bin/pip install -r requirements.txt
	touch dev_env/timestamp
dev_env: dev_env/timestamp
