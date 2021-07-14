# Coffee Shop Full Stack

## Introduction

Uda-Spice Latte Cafe is a full stack drink menu application.  
Features:  
1. Displays graphics representing the ratios of ingredients in each drink.
2. Allows public users to view drink names and graphics.
3. Allows baristas to see the recipe information.
4. Allows the shop managers to create new drinks and edit existing drinks.


## Tech Stack (Dependencies)

 Besides **Python 3**, here are the other required components:

### 1. Backend Dependencies

 * **Conda** to manage dependencies
 * **SQLAlchemy ORM** as the ORM library of choice
 * **SQLite** for data storage
 * **Flask** as the server framework
 * **Jose** for encoding, decoding, and verifying JWTS

 ##### Key Dependencies

To recreate the backend development environment from the `environment.yml` file using Conda, execute:  

```
conda env create -f environment.yml
```

### 2. Frontend Dependencies

* **Ionic** is used as the front-end UI server and any modern browser is required as GUI client.

**Installing Ionic Cli:**  

The Ionic Command Line Interface is required to serve and build the frontend. Instructions for installing the CLI is in the [Ionic Framework Docs](https://ionicframework.com/docs/installation/cli).  

**Installing frontend dependencies**  

This project uses NPM to manage the frontend software dependencies. NPM Relies on the `package.json` file located in the `frontend` directory of this repository. After cloning, open your terminal and run:  

```bash
npm install
```

## Usage:

1. **Run the backend server:**  

first ensure you are working using your created virtual environment.  
Then, from within the `coffee_shop_app/backend/src` directory run:  

```
export FLASK_APP=api.py
flask run --reload
```

2. **Start the frontend server:**  

From inside `/coffee_shop_app/frontend` run the following command:

```
ionic serve
```


3. **Verify on the Browser**  
Navigate to [http://127.0.0.1:8100/](http://127.0.0.1:8100/) or [http://localhost:8100](http://localhost:8100) 


## Acknowledgement  

This Web App is based on the following project starter code:   

```
https://github.com/udacity/FSND/tree/master/projects/03_coffee_shop_full_stack/starter_code
```