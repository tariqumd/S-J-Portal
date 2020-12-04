from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_login import LoginManager
from flask_login import UserMixin,logout_user,current_user,login_required,login_user
from datetime import date,datetime


app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sjp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(app)
#login_manager=LoginManager(app)
#login_manager.init_app(app)
#login_manager.login_view='login'

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('database created!')

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')

#@app.cli.command('db_seed')
#def db_seed():




#Database class

class employee(db.Model):
    ename=db.Column(db.String(60),nullable=False)
    username=db.Column(db.String(60),primary_key=True,nullable=False)
    password=db.Column(db.String(60),nullable=False)
    experience=db.Column(db.Integer,nullable=False)
    skillset= db.Column(db.String(120),nullable=False)
    dob= db.Column(db.String(60),nullable=False)
    location=db.Column(db.String(60),nullable=False)
    phone=db.Column(db.Integer,nullable=False)

class employer(db.Model):
    employername=db.Column(db.String(60),primary_key=True,nullable=False)
    username= db.Column(db.String(60),primary_key=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)

class job_posted(db.Model):
    jobid = db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    employername=db.Column(db.String(60),nullable=False)
    jobtitle=db.Column(db.String(60),nullable=False)
    jobdesc=db.Column(db.String(250),nullable=False)
    joblocation=db.Column(db.String(60),nullable=False)
    skillset= db.Column(db.String(120),nullable=False)
    experience=db.Column(db.Integer,nullable=False)

class applied(db.Model):
    app_id= db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    jobid = db.Column(db.Integer,nullable=False)
    username=db.Column(db.String(60),nullable=False)
    status=db.Column(db.String(60),nullable=False)


from application import routes
if __name__=="__main__":
    app.run(debug=True)
