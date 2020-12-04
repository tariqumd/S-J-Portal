from application import app,db,employee,employer,job_posted,applied
from flask import render_template,request,json,Response, redirect , flash, url_for,session
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import literal

@app.route("/")
@app.route("/index",methods=['GET','POST'])
def index():

    #print(session)
    if session:
        if session['type']=="employee":
            flash("Already Logged in","warning")
            return redirect("employeehome")
        elif session['type']=="employer":
            flash("Already Logged in","warning")
            return redirect("employerhome")

    if request.method == "POST":
        if request.form.get("type") == "employee":
            user=employee.query.filter_by(username=request.form.get("username")).first()
            if user and check_password_hash(user.password,request.form.get("password")):
                session['user']=user.username
                session['name']=user.ename
                session['type']="employee"
                flash(f"{user.ename} Logged In","success")
                return redirect("employeehome")
            else:
                flash("Invalid Credentials","danger")
                session['type']=False
                return redirect("index")

        elif request.form.get("type") == "employer":
            user=employer.query.filter_by(username=request.form.get("username")).first()
            if user and check_password_hash(user.password,request.form.get("password")):
                session['user']=user.username
                session['name']=user.employername
                session['type']="employer"
                flash(f"{user.employername} Logged In","success")
                return redirect("employerhome")
            else:
                flash("Invalid Credentials","danger")
                session['type']=False
                return redirect("index")


    return render_template("index.html",index=True)

@app.route("/logout")
def logout():

    session['user']=""
    session['name']=""
    session['type']=False

    #session.pop('name',None)
    #session.pop('user',None)
    #session.pop('type',None)
    return redirect(url_for('index'))

@app.route("/employeehome",methods=['GET','POST'])
def employeehome():
    if session['type']=="employee":
        criterias=[]
        emp=job_posted.query.all()
        if request.method == "POST":
            emp=""
            title=request.form.get("title")
            ename=request.form.get("ename")
            skill=request.form.get("skills")
            loc=request.form.get("loc")
            exp=request.form.get("exp")
            criterias=[title,ename,skill,loc,exp]

            if title=="" and ename=="" and skill=="" and loc=="" and exp=="": #Excluding all filters
                emp=job_posted.query.all()

            elif title!="" and ename!="" and skill!="" and loc!="" and exp!="": #Including all filters
                emp=job_posted.query.filter(job_posted.employername.contains(ename),job_posted.jobtitle.contains(title),
                job_posted.skillset.contains(skill),job_posted.experience>=exp,job_posted.joblocation.contains(loc))

            elif title!="" and ename=="" and skill=="" and loc=="" and exp=="": #Including 1 filter(title)
                emp=job_posted.query.filter(job_posted.jobtitle.contains(title))


            elif title=="" and ename!="" and skill=="" and loc=="" and exp=="": #Including 1 filter(ename)
                emp=job_posted.query.filter(job_posted.employername.contains(ename))

            elif title=="" and ename=="" and skill!="" and loc=="" and exp=="": #Including 1 filter(skill)
                emp=job_posted.query.filter(job_posted.skillset.contains(skill))

            elif title=="" and ename=="" and skill=="" and loc!="" and exp=="": #Including 1 filter(location)
                emp=job_posted.query.filter(job_posted.joblocation.contains(loc))

            elif title=="" and ename=="" and skill=="" and loc!="" and exp=="": #Including 1 filter(experience)
                emp=job_posted.query.filter(job_posted.experience>=exp)

            #including 2 Filters

            elif title!="" and ename!="" and skill=="" and loc=="" and exp=="": #Including 2 filters (title,name)
                emp=job_posted.query.filter(job_posted.employername.contains(ename),job_posted.jobtitle.contains(title))

            elif title!="" and ename=="" and skill!="" and loc=="" and exp=="": #Including 2 filters (title,skill)
                emp=job_posted.query.filter(job_posted.jobtitle.contains(title),job_posted.skillset.contains(skill))

            elif title!="" and ename=="" and skill=="" and loc!="" and exp=="": #Including 2 filters (title,location)
                emp=job_posted.query.filter(job_posted.jobtitle.contains(title),job_posted.joblocation.contains(loc))

            elif title!="" and ename!="" and skill=="" and loc=="" and exp!="": #Including 2 filters (title,experience)
                emp=job_posted.query.filter(job_posted.jobtitle.contains(title),job_posted.experience>=exp)

            elif title=="" and ename!="" and skill!="" and loc=="" and exp=="": #Including 2 filters (name,skill)
                emp=job_posted.query.filter(job_posted.employername.contains(ename),job_posted.skillset.contains(skill))

            elif title=="" and ename!="" and skill=="" and loc!="" and exp=="": #Including 2 filters (name,location)
                emp=job_posted.query.filter(job_posted.employername.contains(ename),job_posted.joblocation.contains(loc))

            elif title=="" and ename!="" and skill=="" and loc=="" and exp!="": #Including 2 filters (name,experience)
                emp=job_posted.query.filter(job_posted.employername.contains(ename),job_posted.experience>=exp)

            elif title=="" and ename=="" and skill!="" and loc!="" and exp=="": #Including 2 filters (skill,location)
                emp=job_posted.query.filter(job_posted.skillset.contains(skill),job_posted.joblocation.contains(loc))

            elif title=="" and ename=="" and skill!="" and loc=="" and exp!="": #Including 2 filters (skill,experience)
                emp=job_posted.query.filter(job_posted.skillset.contains(skill),job_posted.experience>=exp)

            elif title=="" and ename=="" and skill!="" and loc=="" and exp!="": #Including 2 filters (skill,experience)
                emp=job_posted.query.filter(job_posted.skillset.contains(skill),job_posted.experience>=exp)

            elif title=="" and ename=="" and skill=="" and loc!="" and exp!="": #Including 2 filters (location,experience)
                emp=job_posted.query.filter(job_posted.joblocation.contains(loc),job_posted.experience>=exp)

            #Including 3
            elif title!="" and ename!="" and skill!="" and loc=="" and exp=="": #Including 3 filters (Title,name,skill)
                emp=job_posted.query.filter(job_posted.employername.contains(ename),job_posted.jobtitle.contains(title),
                job_posted.skillset.contains(skill))

            elif title!="" and ename!="" and skill=="" and loc!="" and exp=="": #Including 3 filters(Title,name,locations)
                emp=job_posted.query.filter(job_posted.employername.contains(ename),job_posted.jobtitle.contains(title),
                job_posted.joblocation.contains(loc))

            elif title!="" and ename!="" and skill!="" and loc!="" and exp!="": #Including 3 filters(Title,name,experience)
                emp=job_posted.query.filter(job_posted.employername.contains(ename),job_posted.jobtitle.contains(title),
                job_posted.experience>=exp)

            elif title!="" and ename=="" and skill!="" and loc!="" and exp=="": #Including 3 filters(Title,skill,location)
                emp=job_posted.query.filter(job_posted.jobtitle.contains(title),
                job_posted.skillset.contains(skill),job_posted.joblocation.contains(loc))

            elif title!="" and ename=="" and skill!="" and loc=="" and exp!="": #Including 3 filters(title,skill,experience)
                emp=job_posted.query.filter(job_posted.jobtitle.contains(title),
                job_posted.skillset.contains(skill),job_posted.experience>=exp)

            elif title!="" and ename=="" and skill=="" and loc!="" and exp!="": #Including 3 filters(title,location,experience )
                emp=job_posted.query.filter(job_posted.jobtitle.contains(title),
                job_posted.experience>=exp,job_posted.joblocation.contains(loc))

            elif title=="" and ename!="" and skill!="" and loc!="" and exp=="": #Including 3 filters(name,skill,location)

                emp=job_posted.query.filter(job_posted.employername.contains(ename),
                job_posted.skillset.contains(skill),job_posted.joblocation.contains(loc))

            elif title=="" and ename!="" and skill!="" and loc=="" and exp!="": #Including 3 filters(name,skill,experience)
                emp=job_posted.query.filter(job_posted.employername.contains(ename),job_posted.skillset.contains(skill),job_posted.experience>=exp)

            elif title=="" and ename!="" and skill=="" and loc!="" and exp!="": #Including 3 filters(name,location,experience)
                emp=job_posted.query.filter(job_posted.employername.contains(ename),
                job_posted.joblocation.contains(loc),job_posted.experience>=exp)

            elif title=="" and ename=="" and skill!="" and loc!="" and exp!="": #Including 3 filters(skill,location,experience)
                emp=job_posted.query.filter(job_posted.skillset.contains(skill),
                job_posted.joblocation.contains(loc),job_posted.experience>=exp)

            #Including 4

            elif title=="" and ename!="" and skill!="" and loc!="" and exp!="": #Excluding 1 filter(title)
                emp=job_posted.query.filter(job_posted.employername.contains(ename),
                job_posted.skillset.contains(skill),job_posted.experience>=exp,job_posted.joblocation.contains(loc))

            elif title!="" and ename=="" and skill!="" and loc!="" and exp!="": #Excluding 1 filter(ename)
                emp=job_posted.query.filter(job_posted.jobtitle.contains(title),
                job_posted.skillset.contains(skill),job_posted.experience>=exp,job_posted.joblocation.contains(loc))

            elif title!="" and ename!="" and skill=="" and loc!="" and exp!="":#Excluding 1 filter(skill)
                emp=job_posted.query.filter(job_posted.employername.contains(ename),job_posted.jobtitle.contains(title),
                job_posted.experience>=exp,job_posted.joblocation.contains(loc))


            elif title!="" and ename!="" and skill!="" and loc=="" and exp!="": #Excluding 1 filter(location)
                emp=job_posted.query.filter(job_posted.employername.contains(ename),job_posted.jobtitle.contains(title),
                job_posted.skillset.contains(skill),job_posted.experience>=exp)


            elif title!="" and ename!="" and skill!="" and loc!="" and exp=="": #Excluding 1 filter(experience)
                emp=job_posted.query.filter(job_posted.employername.contains(ename),job_posted.jobtitle.contains(title),
                job_posted.skillset.contains(skill),job_posted.joblocation.contains(loc))

        return render_template("employeehome.html",employeehome=True,employer=emp,filters=criterias)
    else:
        flash("Invalid access","warning")
        return redirect("index")


@app.route("/employerhome",methods=['GET','POST'])
def employerhome():
    criterias=[]
    if session['type']=="employer":
        emp=employee.query.all()
        if request.method == "POST":
            emp=""
            skill=request.form.get("skills")
            loc=request.form.get("loc")
            exp=request.form.get("exp")
            criterias=[skill,loc,exp]

            if skill=="" and loc=="" and exp=="":
                emp=employee.query.all()
            elif skill!="" and loc!="" and exp!="":
                emp=employee.query.filter(employee.skillset.contains(skill),employee.experience>=exp,employee.location.contains(loc))
            elif skill!="" and loc=="" and exp!="":
                emp=employee.query.filter(employee.skillset.contains(skill),employee.experience>=exp)
            elif skill!="" and exp=="" and loc!="":
                emp=employee.query.filter(employee.skillset.contains(skill),employee.location.contains(loc))
                #print(skill,loc)
            elif loc!="" and skill=="" and exp!="":
                emp=employee.query.filter(employee.experience>=exp,employee.location.contains(loc))
            elif skill!="" and loc=="" and exp=="":
                emp=employee.query.filter(employee.skillset.contains(skill))
            elif skill=="" and loc!="" and exp=="":
                emp=employee.query.filter(employee.location.contains(loc))
            elif skill=="" and loc=="" and exp!="":
                emp=employee.query.filter(employee.experience>=exp)

            #if emp.ename=="":
            #print(emp.ename)

        return render_template("employerhome.html",employerhome=True,employee=emp,filters=criterias)
    else:
        flash("Invalid access","warning")
        return redirect("index")



@app.route("/postjob",methods=['GET','POST'])
def postjob():
    if session['type']=="employer":

        if request.method=="POST":
            db.session.add_all([
                        job_posted(employername=session['name'],jobtitle=request.form.get("jobtitle"),jobdesc=request.form.get("jobdesc"),
                                joblocation=request.form.get("location"),skillset=request.form.get("skillset"),experience=request.form.get("minexp"))
                                ])
            db.session.commit()
            flash("Job Posted","success")
            return redirect("postjob")


        return render_template("postjob.html",postjob=True)
    else:
        flash("Invalid access","warning")
        return redirect("index")

'''

@app.route("/applied",methods=['GET','POST'])
def applied():
    if session and session['type']=="employee":
        if request.method=="POST":
            if request.form.get("formname")=="apply":
                i=0
                print(request.form.get("id"),session['user'])
                apply=applied(app_id=i+1,jobid=request.form.get("id"),username=session['user'],status="Applied")

                db.session.add(apply)
                db.session.commit()
                i=i+1
                flash("Applied","success")
                return redirect("employeehome")


    else:
        flash("Invalid access","warning")
        return redirect("index")

'''

@app.route("/edjobs",methods=['GET','POST'])
def edjobs():
    if session['type']=="employer":
        if request.method=="POST":
            if request.form.get("formname")=="delete":
                #print(request.form.get("id"))
                job_posted.query.filter( job_posted.jobid==request.form.get("id")).delete()
                db.session.commit()

                return redirect("jobsposted")

            if request.form.get("formname")=="edit":
                mode="Edit"
                print(mode)
                jobs=job_posted.query.filter_by(jobid=request.form.get("id")).first()

                return render_template("postjob.html",jobsposted=True,jobs=jobs,mode=mode)

            if request.form.get("formname")=="save":
                jobs=job_posted.query.filter_by(employername=request.form.get("empname")).first()

                jobs.jobtitle=request.form.get("jobtitle")
                jobs.jobdesc=request.form.get("jobdesc")
                jobs.joblocation=request.form.get("location")
                jobs.skillset=request.form.get("skillset")
                jobs.experience=request.form.get("minexp")

                db.session.commit()
                flash("Job Saved","success")
                return redirect("jobsposted")
    else:
        flash("Invalid access","warning")
        return redirect("index")



@app.route("/jobsposted",methods=['GET','POST'])
def jobsposted():
    if session['type'] == "employer":
        print(session['name'],session['user'])
        jobs=job_posted.query.filter_by(employername=session['name']).all()
        print(jobs)


        return render_template("jobsposted.html",jobsposted=True,jobs=jobs)
    else:
        flash("Invalid access","warning")
        return redirect("index")

@app.route("/editemployer",methods=['GET','POST'])
def editemployer():
    if session['type'] == "employer":
        emp=employer.query.filter_by(employername=session['name']).first()
        #print(jobs)
        if request.method=="POST":
            if request.form.get("formname")=="employerdetails":
                job=job_posted.query.filter_by(employername=emp.employername).all()
                print(job)
                for i in job:
                    i.employername=request.form.get("empname")
                emp.employername=request.form.get("empname")
                emp.username=request.form.get("username")
                db.session.commit()
                session['name']=emp.employername
                session['user']=emp.username
                flash("Changes saved","success")
                return redirect("editemployer")

        if request.method=="POST":
            if request.form.get("formname")=="password":
                if check_password_hash(emp.password,request.form.get("oldpass")):
                    if request.form.get("newpass") == request.form.get("newpasscnf"):
                        emp.password=generate_password_hash(request.form.get("newpass"))
                        db.session.commit()
                        flash("Password changed successful","success")
                        return redirect("editemployer")
                    else:
                        flash("Password doesnt match","warning")
                        return redirect("editemployer")
                else:
                    flash("Wrong password","danger")
                    return redirect("editemployer")



        return render_template("editemployer.html",editemployer=True,emp=emp)
    else:
        flash("Invalid access","warning")
        return redirect("index")

@app.route("/editemployee", methods=['GET', 'POST'])
def editemployee():
    if session['type'] == "employee":
        emp = employee.query.filter_by(ename=session['name']).first()

        if request.method == "POST":
            if request.form.get("formname") == "employeedetails":
                emp.ename = request.form.get("empname")
                emp.username = request.form.get("username")
                emp.skillset = request.form.get("skillset")
                emp.experience = request.form.get("experience")
                emp.dob = request.form.get("dob")
                emp.location = request.form.get("location")
                emp.phone = request.form.get("phone")
                db.session.commit()
                session['name'] = emp.ename
                session['user'] = emp.username
                flash("Changes saved", "success")
                return redirect("editemployee")

        if request.method == "POST":
            if request.form.get("formname") == "password":
                if check_password_hash(emp.password, request.form.get("oldpass")):
                    if request.form.get("newpass") == request.form.get("newpasscnf"):
                        emp.password = generate_password_hash(request.form.get("newpass"))
                        db.session.commit()
                        flash("Password changed successful", "success")
                        return redirect("editemployee")
                    else:
                        flash("Password doesnt match", "warning")
                        return redirect("editemployee")
                else:
                    flash("Wrong password", "danger")
                    return redirect("editemployee")

        return render_template("editemployee.html",editemployee=True,emp=emp)
    else:
        flash("Invalid access","warning")
        return redirect("index")


@app.route("/registeremployee",methods=['GET','POST'])
def registeremployee():
    if session['type']=="employee":
        flash("Already Logged in","warning")
        return redirect("employeehome")
    elif session['type']=="employer":
        flash("Already Logged in","warning")
        return redirect("employerhome")

    if request.method=="POST":
        username=employee.query.filter_by(username=request.form.get("username")).scalar()
        if username == None:
            db.session.add_all([
                            employee(ename=request.form.get("empname"),username=request.form.get('username'),
                            password=generate_password_hash(request.form.get('password')),experience=request.form.get('experience'),
                            skillset=request.form.get('skillset'),dob=request.form.get('dob'),location=request.form.get("location")
                            ,phone=request.form.get('phone'))
                                    ])
            db.session.commit()
            flash("Signup successfull","success")
            return redirect("index")

        else:
            flash("username not available","warning")
            return redirect("registeremployee")


    return render_template("register_employee.html",register_employee=True)

@app.route("/registeremployer",methods=['GET','POST'])
def registeremployer():
    if session['type']=="employee":
        flash("Already Logged in","warning")
        return redirect("employeehome")
    elif session['type']=="employer":
        flash("Already Logged in","warning")
        return redirect("employerhome")

    if request.method=="POST":
        en=employer.query.filter_by(employername=request.form.get("employername")).scalar()
        if en == None:
            username=employer.query.filter_by(username=request.form.get("username")).scalar()
            if username == None:
                db.session.add_all([
                                    employer(employername=request.form.get("employername"),
                                    username=request.form.get("username"),password=generate_password_hash(request.form.get("password"))) ])
                db.session.commit()
                flash("Signup successfull","success")
                return redirect("index")
            else:
                flash("username not available","warning")
                return redirect("registeremployer")
        else:
            flash("employer name already registered","warning")
            return redirect("registeremployer")



    return render_template("register_employer.html",register_employer=True)
