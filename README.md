# django-todoapp
Interview task - simple Todo app (tasks)

## Installation

* `docker-compose up`
* `docker-compose exec app python src/manage.py migrate`
* `docker-compose exec app python src/manage.py createsuperuser` [test, test]

Then visit: `http://localhost:8000/tasks/`

## Usage

### Filtering

* `/tasks/?due_date__gt=2026-01-20`
