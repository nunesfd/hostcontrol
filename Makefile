start:
	python main.py

start-dev:
	export APP_ENV=development; \
	export HOSTCTL_HOSTS_PATH="./data/hosts"; \
	export HOSTCTL_DB_PATH="./data/.host_control"; \
	textual run --dev main.py

start-console:
	textual console -x SYSTEM -x EVENT -x DEBUG -x INFO