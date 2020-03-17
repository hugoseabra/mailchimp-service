DOCKER_COMPOSE_ENV=conf/docker-compose_dev.yml
CELERY_SERVICES=-A project
CELERY_PID_FILE=/tmp/celery.pid
CELERY_LOG_FILE=/tmp/broker.log
NOW=$(shell date --iso=seconds)
DOCKER_REPO=871800672816.dkr.ecr.us-east-1.amazonaws.com
DOCKER_IMAGE_NAME=mailchimp-service
DOCKERFILE=conf/Dockerfile

# Inicializa ambiente
.PHONY: init
up:
	@make update-db
	@make add-fixtures
	@echo "\nAddress: http://localhost:8000/admin"
	@echo "Credentials:\n  - user: admin\n  - pass: 123"
	@make start-services

# Remove serviços e banco de dados.
.PHONY: down
down: del-dev-migrations destroy-services
	rm -f db.sqlite3

.PHONY: start-services
start-services: broker_create
	docker-compose -f $(DOCKER_COMPOSE_ENV) up -d --remove-orphans;

.PHONY: stop-services
stop-services:
	docker-compose -f $(DOCKER_COMPOSE_ENV) stop;

.PHONY: destroy-services
destroy-services: broker_kill
	docker-compose -f $(DOCKER_COMPOSE_ENV) down;

.PHONY: logs
logs:
	docker-compose -f $(DOCKER_COMPOSE_ENV) logs -f

.PHONY: stop
stop:
	docker-compose -f $(DOCKER_COMPOSE_ENV) stop


.PHONY: services
services:
	docker-compose -f $(DOCKER_COMPOSE_ENV) ps

# Atualiza banco de dados migrando para uma nova versão disponível.
.PHONY: update-db
update-db:
	./manage.py makemigrations
	./manage.py migrate

# Adiciona fixtures
.PHONY: add-fixtures
add-fixtures:
	./manage.py loaddata 000_site_dev
	./manage.py loaddata 000_admin
	./manage.py loaddata 000_namespace-namespace
	./manage.py loaddata 001_namespace-listfield
	./manage.py loaddata 001_audience-member
	./manage.py loaddata 002_audience-memberfield

# Remove migrations que não foram adicionados.
.PHONY: del-dev-migrations
del-dev-migrations:
	git status --porcelain | grep "^?? "  | sed -e 's/^[?]* //' | \egrep "\migrations/00*"  | xargs -n1 rm -f

.PHONY: generate-models-diagram
generate-models-diagram:
	mkdir -p ./docs/models-diagram/
	./manage.py graph_models --pydot -a -g -o ./docs/models-diagram/models-diagram-$(NOW).png

.PHONY: test
test:
	mkdir -p ./docs/coverage/
	coverage run manage.py test
	coverage html -d ./docs/coverage/

.PHONY: open-coverage
open-coverage: test
	xdg-open ./docs/coverage/index.html


.PHONY: save-fixtures
save-fixtures:
	./manage.py dumpdata namespace.namespace > namespace/fixtures/000_namespace-namespace.json
	./manage.py dumpdata namespace.listfield > namespace/fixtures/001_namespace-listfield.json
	./manage.py dumpdata audience.member > audience/fixtures/001_audience-member.json
	./manage.py dumpdata audience.memberfield > audience/fixtures/002_audience-memberfield.json

.PHONY: broker_create
broker_create: broker_kill
	celery -E $(CELERY_SERVICES) worker -B -l INFO --scheduler django -s /tmp/beat-scheduler --logfile="$(CELERY_LOG_FILE)" --pidfile="$(CELERY_PID_FILE)" --detach;

.PHONY: broker_kill
broker_kill:
	ps x --no-header -o pid,cmd | awk '!/awk/&&/celery/{print $$1}' | xargs -r kill
	rm -f $(CELERY_PID_FILE)

.PHONY: broker_restart
broker_restart:
	@make broker_kill
	@make broker_create

.PHONY: broker_debug
broker_debug: broker_kill
	celery -E $(CELERY_SERVICES) worker -B -l INFO --scheduler django -s /tmp/beat-scheduler --logfile="$(CELERY_LOG_FILE)" --pidfile="$(CELERY_PID_FILE)";

.PHONY: broker_follow_log
broker_follow_log:
	touch $(CELERY_LOG_FILE)
	tail -f  $(CELERY_LOG_FILE)

.PHONY: build-image
build-image:
	@docker build --compress --rm -f $(DOCKERFILE) -t $(DOCKER_REPO)/$(DOCKER_IMAGE_NAME):latest .

.PHONY: push-image
push-image:
	@docker start awsecr
	@docker exec awsecr push $(DOCKER_IMAGE_NAME)
