## API Inventory Food


## Version 1.0.0

## License

This project is released under the [MIT license](https://github.com/).

## Author
Edgar Aldana

## How to use this API

The API documentation is available at https://api-food-inventory.onrender.com/docs & https://api-food-inventory.onrender.com/redoc

## Requirements

python 3.10.X

```bash
pip install -r requirements.txt

``` 

# add .env file

## content example

```bash

DATABASE_NAME='database-inventory-food.db'

SECRET_KEY='secret_key'
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRES_MINUTES=30

```


# run app fastapi

```bash

cd app
fastapi dev food-inventory.py --reload --host 0.0.0.0 --port 8000

```



