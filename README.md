## Workmate-Django-DRF
### Project Description

This project is an online kitten exhibition where users can register, add their kittens, rate them and leave comments. The main goal of the project is to create an interactive platform for hobbyists where they can share information, participate in exhibitions and rate other users' kittens.

Main features:

1. User Registration:
- Users can register by providing their email, name and other details. Two roles are available: 'participant' and 'visitor'.
2. Breed Management:
- Users with the “participant” role can add, edit and delete breeds.
3. Creation Management:
- Users can add information about their kittens, including color, name, age, and description. Kittens are linked to breeds and owners.
4. Evaluation:
- Users can leave ratings and comments. Scores can range from 1 to 5.
4. Filtering and searching:
- Ability to filter kittens by breed.
5. Statistics:
- Ability to get statistics of scores for each kitten.

### Technology and libraries
* [Python 3.10.12](https://www.python.org/doc/)
* [Django 5.1.1](https://docs.djangoproject.com/en/4.2/)
* [Django REST Framework  3.15.2](https://www.django-rest-framework.org/)
* [djangorestframework-simplejwt 5.3.1](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
* [PostgreSQL 14](https://www.postgresql.org/docs/14/index.html)
* [pytest-xdist 3.6.1](https://pytest-xdist.readthedocs.io/en/stable/)
* [pytest-django 4.9.0](https://pytest-django.readthedocs.io/en/latest/index.html)
* [pytest-factoryboy 2.7.0](https://pytest-factoryboy.readthedocs.io/en/stable/)
* [Docker-Compose](https://docs.docker.com/compose/release-notes/)

## Installation on local computer
### 1. Clone the repository:

```
git clone https://github.com/minkeviiich/Online_exhibition-Workmate--Django-DRF.git
```
### 2. Build a Docker image: (Commands are automated using Makefile)

- Build the Docker image

```
make build
```

### 3. Starting Docker Compose:

```
make up
```
### 4. Running Tests: (Note: the make test command runs tests using pytest-xdist, spreading their execution over 4 processors/core. The value can be changed in the Makefile)

```
make test
```
### 5. Stopping and removing containers:

```
make down
```

### __OpenAPI documentation__
* Swagger: http://0.0.0.0:8000/swagger/
