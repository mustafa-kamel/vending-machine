# Python Vending Machine
Web APIs that simulates a vending machine behaviour.

The app consists of RESTful APIs for managing users (registration, authentication, authorization) and Products CRUD.
The users can register a new account and use it to add deposit and buy from the vending machine, the users can have one of two types (seller or buyer) a seller can manage products and a buyer can add deposit and buy a product.

## Requirements
* Python >= 3.8
* Django >= 3.2


## Included Features
- User CRUD.
- API Authentecation using JWT token.
- Authorization using user roles.
- Product CRUD for Sellers.
- Add/Reset deposit for Buyers.
- Buy a product for Buyers.
- 100% Test coverage.
- The app is dockerized.


## Installation
1. Clone the project.
```bash
git clone https://github.com/mustafa-kamel/vending-machine.git
```
2. Change the active directory to the project directory.
```bash
cd vending-machine
```
3. Create a virtual environment.
```bash
python3 -m venv venv
```
4. Activate the virtual environment.
```bash
source venv/bin/activate
```
5. Install the app requirements.
```bash
pip install -r requirements.txt
```
6. Run the migrations.
```bash
./manage.py migrate
```
7. Run the local server.
```bash
./manage.py runserver
```
1. The app should now be accessible through [http://localhost:8000](http://localhost:8000/).


Or simply you can run the app in a docker container.

1. Build the docker image.
```bash
docker build -t vending:latest .
```
2. Run the container.
```bash
docker run -it -p 8000:8000 vending:latest .
```



## Testing
Their is test coverage to almost all possible scenarios.

To test the app is working properly run the following command:
```bash
./manage.py test
```


## APIs
API documentation is available [here](https://documenter.getpostman.com/view/1861377/UVkvJCUt)


## License
This software is licensed under the `MIT License`. See the ``LICENSE``
file in the top distribution directory for the full license text.
