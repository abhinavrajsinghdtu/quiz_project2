import os

from flask import Flask
from flask import render_template
from flask import request, flash
from flask_sqlalchemy import SQLAlchemy 
from flask import redirect

import random
from sqlalchemy.sql.expression import func,select


app = Flask(__name__)


# databaseConn
project_dir = os.path.dirname(os.path.abspath(__file__))

database_file = "sqlite:///{}".format(os.path.join(project_dir,"quizdatabase.db"))

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"]="randomString"

db = SQLAlchemy(app)



#schema
# A database schema is considered as the blueprint of a database
#  which describes how the data may relate to other tables or other data models

class MCQ(db.Model):

    sno = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
    question = db.Column(db.String(10000),unique=True, nullable=False)
    option1 = db.Column(db.String(1000), nullable=False)
    option2 = db.Column(db.String(1000), nullable=False)
    option3 = db.Column(db.String(1000), nullable=False)
    option4 = db.Column(db.String(1000), nullable=False)
    answer = db.Column(db.String(1000), nullable=False)

    def __init__(self,question,option1,option2,option3,option4,answer):
        self.question=question
        self.option1=option1
        self.option2=option2
        self.option3=option3
        self.option4=option4
        self.answer=answer


class User(db.Model):
    uid = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100),unique=True, nullable=False)
    password = db.Column(db.String(100),nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    result = db.Column(db.Integer(), nullable=False)

    def __init__(self,username,email,password,phone,result):
        self.username = username
        self.email = email
        self.password = password
        self.phone = phone
        self.result = result


# @app.route("/login" , methods=["GET", "POST"])
# def login():

#     if request.method=="POST" and "username" in request.form and "password" in request.form:

        
#         if not request.form["email"] or not request.form["psw"]:
#             # flash("Please enter all the fields","error")
#             print("Please enter all the fields")
#             return redirect("/login")

#         else:
            

#             # flash("MCQ was added successfully")
#             print("Login was successfully") 
#             return redirect("/admin")
   
#     return render_template("login/login.html",mcq=mcq)



# Routing is a technique used by modern web apps.
#  This helps the user remember the URLs
# E.g., if my site’s domain was www.localit.org and I want to add routing to “www.localit.org/hello”, I can use “/hello”.
 

# GET Request-----> A GET message is sent, and the server returns data
# POST Request----> Used to send HTML form data to the server


# Register

@app.route("/register" , methods = ["GET", "POST"])
def register():
    if request.method=="POST":

        if not request.form["email"] or not request.form["username"] or not request.form["phone"] or not request.form["password"]:
            print("Please enter correct details")
            # flash('Please enter correct details','error')
            return redirect("/register")

        else:
            print(request.form["username"])
            print(request.form["email"])
            print(request.form["password"])
            print(request.form["phone"])
            result=0
            user = User(request.form["username"],request.form["email"],request.form["password"],request.form["phone"],result)
            db.session.add(user)
            db.session.commit()
            # flash("registered successfully")
            return redirect("/quiz")

    return render_template("login/register.html")


# Login
check_email=""
@app.route("/" , methods=["GET", "POST"])
def login():
    print("check")
    global check_email
    if request.method=="POST":
        print(request.form["email"])
        print(request.form["psw"])
        if not request.form["email"] or not request.form["psw"]:
            print("Please enter correct details")
            # flash('Please enter correct details')

        else:

            email = request.form["email"]
            user = User.query.filter_by(email=email).first()
            print(user.email)
            print(user.password)
            if(user.password==request.form["psw"]):
                print("Login Successfull")
                check_email = user.email
                return redirect("/quiz")
            
    
    return render_template("login/login.html")
    


#CRUD Operations----> Create, Read, Update and Delete

@app.route("/admin",methods=["GET","POST"])
def home():
    if request.method=="POST":
        # print(request.form)
        if not request.form["question"] or not request.form["option1"] or not request.form["option2"] or not request.form["option3"] or not request.form["option4"] or not request.form["answer"]:
            # flash("Please enter all the fields","error")
            print("Please enter all the fields")
            return redirect("/admin")

        else:
            rows = db.session.query(MCQ).count() #no of rows in database
            mcq = MCQ(request.form["question"],request.form["option1"],request.form["option2"],request.form["option3"],request.form["option4"],request.form["answer"])
            db.session.add(mcq)
            db.session.commit()

            # flash("MCQ was added successfully")
            print("MCQ was added successfully") 
            # return redirect("/admin")
    userList = User.query.all()   
    mcqList =MCQ.query.all()
    print(len(userList))
    print(len(mcqList))
    return render_template("admin.html",mcqList=mcqList,userList=userList)



@app.route("/update",methods=["POST"])
def update():
    # newtitle = request.form.get("new_title")
    # oldtitle = request.form.get("old_title")
    # mcq = MCQ.query.filter_by(title=oldtitle).first()
    # mcq.title=newtitle
    newQuestion = request.form.get("new_question")
    newOption1 = request.form.get("new_option1")
    newOption2 = request.form.get("new_option2")
    newOption3 = request.form.get("new_option3")
    newOption4 = request.form.get("new_option4")
    newAnswer = request.form.get("new_answer")

    oldQuestion = request.form.get("old_question")
    mcq = MCQ.query.filter_by(question=oldQuestion).first()
    if request.form["new_question"]:
        mcq.question=newQuestion

    if request.form["new_option1"]:
        mcq.option1=newOption1

    if request.form["new_option2"]:
        mcq.option2=newOption2

    if request.form["new_option3"]:
        mcq.option3=newOption3

    if request.form["new_option4"]:
        mcq.option4=newOption4

    if request.form["new_answer"]:
        mcq.answer=newAnswer

    db.session.commit()
    return redirect("/admin")


@app.route("/delete",methods=["POST"])
def delete():
    question = request.form.get("del_question")
    mcq = MCQ.query.filter_by(question=question).first()
    db.session.delete(mcq)
    db.session.commit()
    return redirect("/admin")


result=0
rowCount=0
questionDisplayedCount=0
questionDisplayed=[]


@app.route("/quiz",methods=["GET","POST"])
def quiz():
    # randomList = random.sample(range(1,11),10)
    # for i in randomList:
    #     print(i)

    
    global questionDisplayed
    if request.method=="POST":
        global questionDisplayedCount,result,rowCount
        questionDisplayedCount+=1
        rowCount = db.session.query(MCQ).count()      #no of rows in database
        print(rowCount)
        answer = request.form["check_answer"]
        print(answer)
        if answer==request.form["option"]:
            result+=1
        if rowCount==questionDisplayedCount:
            return redirect("/result")
        return redirect("/quiz")

    
    try:
        mcq = db.session.query(MCQ).order_by(func.random()).first()
        print(mcq.question)
    except:
        return ("There is no question in Quiz database")
    
    if questionDisplayed.__contains__(mcq.question):
        return redirect("/quiz")
    questionDisplayed.append(mcq.question)
    return render_template("quiz.html",mcq=mcq,number=questionDisplayedCount+1)



@app.route("/result",methods=["GET","POST"])
def results():

    global result,rowCount
    if request.method == "POST":
        # print(request.form["result"])
        print(result)
        user = User.query.filter_by(email=check_email).first()
        user.result = result
        db.session.commit()
        return redirect("/")
        
    return render_template("result.html",result=result,rowCount=rowCount)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

