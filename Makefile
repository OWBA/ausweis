SSH ?= vps3:~/ausweis-docker

.PHONY: help
help:
	@echo 'defaults: SSH=$(SSH)'
	@echo
	@echo 'available commands:'
	@echo ' - for docker: start, stop, nuke, init, gen-key'
	@echo ' - for rsync:  push [SSH=xxx]'

# ----------
#   docker
# ----------

.PHONY: init
init:
	docker-compose exec app sh /django_project/scripts/on-init.sh

.PHONY: gen-key
gen-key:
	docker-compose exec app python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

.PHONY: start
start:
	docker-compose up -d --force-recreate

.PHONY: stop
stop:
	docker-compose stop

.PHONY: nuke
nuke:
	docker rm ausweis || true
	docker network rm ausweis || true
	docker image rm ausweis || true

# ----------
#   rsync
# ----------

.PHONY: push
push:
	rsync -av --delete --exclude=backend/data --exclude=.venv --exclude=.git --exclude=.DS_Store \
		backend docker-compose.yml Makefile \
		$(SSH)/
