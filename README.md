# TODO_project
Test work

Task: Write REST API for TODO-list:
- without authorization;
- use Django, Django Rest Framework, PostgreSQL
- run in Docker
- pull progect on GitHub with instructions.


## Getting Started

Download links:

SSH clone URL: git@github.com:bekaryukovmv/TODO_project.git

HTTPS clone URL: https://github.com/bekaryukovmv/TODO_project.git


These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Local setup

+ cloning project
```shell script
git clone https://github.com/bekaryukovmv/TODO_project.git
```

+ environment set up

```shell script
cd project_dir
cp project.env.template .env
```
Fill the blank lines your real env data.

+ running
```shell script
docker-compose up -d --build
```

+ applying all migrations
```shell script
docker-compose exec django_todo python manage.py migrate
```

+ Optional (for use django rest framework visual interface)
```shell script
docker-compose exec django_todo python manage.py collectstatic
```

+ Run tests
```shell script
docker-compose exec django_todo python manage.py test
```


Congratulations! Your local fmm api is ready to use.


API-endpoints:
1) GET http://0.0.0.0/api/v1/lists/  - get TODO lists
2) POST http://0.0.0.0/api/v1/lists/  - create new TODO List
3) GET http://0.0.0.0/api/v1/lists/UUID/- get single TODO List
4) DELETE http://0.0.0.0/api/v1/lists/UUID/ - Delete TODO list

5) GET http://0.0.0.0/api/v1/lists/UUID/items/ - get List of TODOList Items
6) POST http://0.0.0.0/api/v1/lists/UUID/items/ - create TODOList Item
7) GET http://0.0.0.0/api/v1/lists/List_UUID/items/Item_UUID/ - get single Item
8) PUT\PATCH http://0.0.0.0/api/v1/lists/{List_UUID}/items/{Item_UUID}/ - update single Item
9) DELETE http://0.0.0.0/api/v1/lists/{List_UUID}/items/{Item_UUID}/ - delete single Item

10) GET http://0.0.0.0/api/v1/item-status-choices/ - get item status choices.
