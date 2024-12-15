run-migration:
	alembic upgrade head && alembic revision --autogenerate -m 'Initial migration'

run-docker:
	docker-compose up -d

stop-docker:
	docker-compose down
	docker rmi clinic

tests:
	export PYTHONPATH=$(pwd)
	pytest