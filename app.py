from flask import Flask,send_from_directory,session,render_template,request
from flask_mysqldb import MySQL
from pytz import timezone
from extensions import mysql 
# from flask_ngrok import run_with_ngrok
#from models.webmodels import Models as db
#import jwt  

_secret_key="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lIjoicGF5bG9hZCJ9.Joh1R2dYzkRvDkqv3sygm5YyK8Gi4ShZqbhK2gxcs2U"

import os
from dotenv import load_dotenv

env = "dev"

if env == "dev":
   load_dotenv("env/dev.env")
elif env == "qa":
    load_dotenv("env/qa.env")
elif env == "demo":
    load_dotenv("env/demo.env")
elif env == "preprod":
    load_dotenv("env/preprod.env")
elif env == "prod":
    load_dotenv("env/prod.env")    
else:
    raise ValueError("Invalid environment specified")


app = Flask(__name__)
# run_with_ngrok(app)


app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
     
port=os.getenv('PORT') 

mysql=MySQL(app)


app.secret_key = "asduqwueqweHBWEHQJ&!GBH#!HE*(#@*EBbBbmm1231DQD1@!"


@app.after_request
def after_request(response):
   response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
   response.headers["Expires"] = 0
   response.headers["Pragma"] = "no-cache"
   return response

@app.after_request
def after_request(response):
   response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
   response.headers["Expires"] = 0
   response.headers["Pragma"] = "no-cache"
   return response

@app.route('/', methods=['POST','GET'])
def home():
    return render_template("index.html")

@app.errorhandler(404) 
def not_found(e): 
  return render_template("index.html")


# @app.errorhandler(404)
# def notfounf():
#     return render_template("index.html")


from routes.admin_routes import api

app.register_blueprint(api)


if __name__ == '__main__':
    # appp=create_app(application)
    app.run(debug=True,host='0.0.0.0',port=port)