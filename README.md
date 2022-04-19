The project is current installable, to install the project as a pip 
Run the below command in the project directory and in the virtual environment  

pip install -e .

Then activate vritual environment using below command 

. venv/bin/activate

Export enviornment variables for flask 

export FLASK_APP=flaskr 

Finally run 

flask run 

More details here - https://flask.palletsprojects.com/en/2.1.x/tutorial/install/ 

# to-do-list-app dev setup 
Usage for mac, on your terminal run the following 

python3 -m venv venv

. venv/bin/activate

pip install Flask

export FLASK_APP=flaskr

export FLASK_ENV=development

flask run


### to init the database ###

flask init-db



#### Endpoints #### 

http://127.0.0.1:5000/hello 


http://127.0.0.1:5000/auth/register


http://127.0.0.1:5000/auth/login


http://127.0.0.1:5000/auth/logout
