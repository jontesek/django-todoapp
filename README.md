# Django Todo app
Interview task - simple Todo app (tasks)

## Setup

* `docker-compose up` - build image and run services (API, DB)
* `docker-compose exec app python src/manage.py migrate` - init DB
* `docker-compose exec app python src/manage.py createsuperuser` - create user (e.g. test, test)

## Usage

API accessible at: `http://localhost:8000/tasks/`

### Endpoints

* GET `/tasks/health/`: Health check
* GET `/tasks/`: List all tasks, filtering available
* POST `/tasks/`: Create new task (provide JSON payload)
* GET, PATCH, DELETE `/tasks/<int>/`: Read, update, delete a given task
* GET `/tasks/<int>/subtasks/`: List all direct subtasks
* GET `/tasks/<int>/subtasks-tree/`: List the whole subtasks tree

### Examples

* Show only completed tasks: `/tasks/?is_completed=true`
* Show tasks with due date before 1. 2. 2026: `/tasks/?due_date__lt=2026-02-01`
* Show tasks with title containing a keyword: `/tasks/?title__icontains=keyword`
* Create new task: POST `/tasks/` (returns id=1)
```json
{"title": "Morning routine", "description": "Prepare for the day", "due_date": "2026-01-25"}
```
* Create new task with parent: POST `/tasks/` (returns id=2)
```json
{"title": "Make tea", "parent": 1}
```
* Set task as completed: PATCH `/tasks/2/`
```json
{"is_completed": true}
```

## Description

### DB model

Only one table `Task` with following attributes:

| Field Name | Data Type | Nullable | Default |
| :--- | :--- | :--- | :--- |
| **id** | int8 (BigInt) | No | Auto-increment |
| **title** | varchar(200) | No | - |
| **description** | text | **Yes** | NULL |
| **due_date** | date | **Yes** | NULL |
| **is_completed** | bool | No | false |
| **created_at** | timestamptz | No | now() |
| **updated_at** | timestamptz | No | now() |
| **parent_id** | int8 (BigInt) | **Yes** | NULL |
| **user_id** | int4 (Integer) | No | logged-in user |

### Hierarchy

Hierarchy is handled by self-referencing: Field `parent_id` connects subtask to its parent task. The foreign key is defined with `ON DELETE CASCADE` so if the parent is deleted, so are all its subtasks.

This solution is simple to implement and to use.
There are other solutions if a better performance would be needed (e.g. Django MPTT).
