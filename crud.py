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
questionDisplayedCount=0
questionDisplayed=[]

@app.route("/",methods=["GET","POST"])
def quiz():
    # randomList = random.sample(range(1,11),10)
    # for i in randomList:
    #     print(i)
    global questionDisplayed
    if request.method=="POST":
        global questionDisplayedCount,result
        questionDisplayedCount+=1
        rowCount = db.session.query(MCQ).count() #no of rows in database
        answer = request.form["check_answer"]
        if answer==request.form["option"]:
            result+=1 
        if rowCount==questionDisplayedCount:
            return ("Your result is: "+str(result)+" / "+str(rowCount))
        return redirect("/")

    mcq = db.session.query(MCQ).order_by(func.random()).first()
    if questionDisplayed.__contains__(mcq.question):
        return redirect("/")
    
    questionDisplayed.append(mcq.question)
    print(mcq.question)
    return render_template("quiz.html",mcq=mcq)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)





