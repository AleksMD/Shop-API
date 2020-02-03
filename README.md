# Shop API
TODO
**Description**
## Getting Started
Please follow the instructions bellow in order to successfully run the API.

## Prerequisites

You should have at least Python version 3.6 and PostgresSQL database installed on your local machine to be able to use this application. 
Preferably to run this app in isolated virtual environment, thus you should
create venv in the beginning:
```
python3 -m venv <name_of_your_venv> # or any other tools

```
All dependencies are listed in **requirements.txt** To install the latter simply enter in either terminal or a prompt the following command:

```
pip install -r requirements.txt

```

## Installing

Clone this repo onto your local machine by the following command:

### https
```
git clone https://github.com/AleksMD/shop_api.git

```
N.B. Database in postgres should be created before you start running the application.
To do so, open postgres db in terminal by this command:

```
sudo -u postgres psql

```
In opened terminal window enter:

```
CREATE DATABASE name_of_your_app_database;

```

Create user in postgres:

```
CREATE USER your_user_name WITH PASSWORD 'your_password';

```

Grant access to the database to the user:
```
GRANT ALL PRIVILEGES ON DATABASE name_of_your_app_database TO your_user_name;
```

After database was created update DATABASE section in settings.py
### Info


## Start API
To start the app activate virtual environment by the following command:

```
source <path_to_virtual_env_folder>/bin/activate

```
and then run following command in terminal in root directory of the project:

```
python manage.py runserver

```
If the start of this app is succussfull you can open an internet browser and go to an index page:

```
http://127.0.0.1:8000/ 

```
If there are no errors it means that everything works fine.

See next section to understand how you run tests.
## API Endpoints

> 

## Testing
There  lots of test cases for this application.
To run all of those use following command:

```
python -m manage test

```
or

```
python manage.py test

```
The difference between both of the above you can find [here.](https://docs.python.org/3/using/cmdline.html)

If you are interested in testing particular test case each test marks by
intuitively undestandable tags. To use that just run the following command:
```

python manage.py test --tag=<tag_name>

```
## Future Development

## Built With

* [Python3.7](https://www.python.org) - The programming language of the app
* [Django REST framework](https://www.django-rest-framework.org/) - The web framework used
* [PostgresSQL](https://rometools.github.io/rome/) - The relational database used

## Versioning

Version 0.0.1

## Authors

* **Oleksandr Budonniy** - *Initial work* - [AleksMD](https://github.com/AleksMD)

## License

Under no license

