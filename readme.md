# GingerEdu Backend

# View Postman Documentation [here](https://documenter.getpostman.com/view/9282395/Uz5Njt54)

_How to run with docker_

## Run

- docker compose build
- docker compose up

---

_How to run without docker_

(If you have python and redis installed, you can skip steps 1 and 2)

1. Install python from [here (preferrably version 3.9.8)](https://www.python.org/downloads/)
2. Install redis from [here](https://redis.io/download/)
3. Create a virtual environment using pipenv, virtualenv or any other tool of your choice
4. Active the environment and run `pip install -r requirements.txt`
5. Create a .env file and copy the environmental variables in env.sample to your .env file
6. Create a postgres database
7. Run `python manage.py migrate && python manage.py makemigrations`
8. Run `python manage.py createsuperuser ` to create a super user admin
9. Run `python manage.py runserver`


## Run Test

- python manage.py test
