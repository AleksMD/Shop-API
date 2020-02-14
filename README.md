# Shop API
Shop REST API is a study project. It was built with raw Django framework and
PostgreSQL as a database. All views are made via functions. It was done
deliberately in order to estimate pros and cons of this approach. 
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

N.B. When running program on local machine database in postgres should be created before you start running the application.
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
You can run app in docker container whether on local machine or VM. Use following
command in terminal:
```
docker-compose up
```
> N.B. Docker compose file include several bash commands that load predefined
> data to the db, including fixtures, thus the first superuser in database has
> following credentials:
```
username: 'admin'
password: 'admin_password'
```
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
If there are no errors and you see some welcome message, it means that everything works fine.

## API Endpoints
*You can use either desktop(Postman, Insomnia etc.) or console(curl, http
etc.) tools for accessing API*
> Sign Up. It creates ordinary user without any special permission. To be able
> to update/create/delete either shops or products you have to create superuser
> prime to start app. Use the following command in terminal:
```
python manage.py createsuperuser
```
and provide app with neccessary data according to the quesions in command
prompt.
Now you are ready to use all functionality of the Shop Api

```
curl -X POST -d "{\"username\": \"<your_username\">, \"email\": \"<your_email>"\, \"password\":\"<your_password>\"}" -H "Content-Type: application/json" \
  http://localhost:8000/signup/
```
> Log In:
```
curl -X POST -d "{\"username\": \"<your_username\">, \"password\":\"<your_password>\"}" -H "Content-Type: application/json" \
  http://localhost:8000/login/
```
*After previous step you will receive csrftoken and sessionid in cookies. To be
able to get access to all resources you should append it to each requests
header(For instance: -H "Set-Cookie: csrftoken=... sessionid=...")* 

> Get lists of all products:
```
http://localhost:8000/products/product-list/
```
 
> Get particular product:
```
http://localhost:8000/products/detail-product/<product_pk>
```
> Add new product(requires admin permissions):
```
http://localhost:8000/products/create_product/
```
> Update info about existing product:
```
http://localhost:8000/products/update_product/<product_id>
```
> Delete product:
```
http://localhost:8000/products/delete-product/<product_id>
```
> Search product with full match:
```
http://localhost:8000/products/exact-search
```
> Search product with particular match:
```
http://localhost:8000/products/approximate-search/
```
> Search by shop:
```
http://localhost:8000/products/search-by-shop/
```
> Search by price range(two fields: 'from', 'to'):
```
http://localhost:8000/products/search-by-price/
```
> Add product to customer's basket:
```
http://localhost:8000/products/add-product-to-basket/<prod_id>
```
> Show active(is not paid yet) basket of current user:
```
http://localhost:8000/baskets/view-active-basket
```
> Show total price of products in basket

```
http://localhost:8000/baskets/view-total-basket-price
```
> Show all baskets (active and not) of current user:
```
http://localhost:8000/baskets/user-basket-list
```
> Pay for basket.
> N.B. This API doesn't use any real payment gateway like(Stripe, PayPal etc.)
> it just emulates process of payment. Client sends json in a look like {'money': <sum_of_money>}
```
http://localhost:8000/baskets/pay-for-basket/
```

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
* [Docker](https://www.docker.com/) - The building environment used
## Versioning

Version 0.0.1

## Authors

* **Oleksandr Budonniy** - *Initial work* - [AleksMD](https://github.com/AleksMD)

## License

Under no license

