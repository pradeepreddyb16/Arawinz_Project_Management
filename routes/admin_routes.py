from flask import Flask,Blueprint,request,jsonify,session
from pytz import timezone
from models.admin_models import models as dbty
import hashlib
import random
import os
import datetime
from models.admin_models import models as db


api=Blueprint('api',__name__,url_prefix='/api')

def getdatetime():
    now = datetime.datetime.now(timezone('Asia/Kolkata'))
    datetimeee=datetime.datetime(
        now.year, now.month, now.day,now.hour,now.minute,now.second)
    datetimee=str(datetimeee)
    return datetimee


def uploadimage(pic, directory):
    now = datetime.datetime.now(timezone('Asia/Kolkata'))
    datetimeee = datetime.datetime(
        now.year, now.month, now.day, now.hour, now.minute, now.second)
    datetimee = str(datetimeee)
    ranNew = str(random.randint(00000, 99999))
    UPLOAD_FOLDER = "static/"+directory+"/"
    ALLOWED_EXTENSIONS = set(
        ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx', 'base64'])
    if pic.filename == 'blob':
        picfilename = datetimee+ranNew+pic.filename+ALLOWED_EXTENSIONS
    else:
        picfilename = datetimee+ranNew+pic.filename
    picfilename = picfilename.replace(":", "")
    picfilename = picfilename.replace("-", "")
    picfilename = picfilename.replace(" ", "")
    picfilename = picfilename.replace(",", "")
    pic.save(os.path.join(UPLOAD_FOLDER, picfilename))
    return picfilename

# user login
@api.route('/user_login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        uname = request.form['uname']
        passs = str(hashlib.md5(request.form['pass'].encode('UTF-8')).hexdigest())
        current_date=getdatetime()
        data=db.checkuserlogin(uname,passs)
        ## Different date with Correct Password
        if data and data['login_atempts']>=5 and data['login_date']!=current_date:
            db.resetpasswordattemptwithuname(uname)

        if data:
            print(data)
            if data['login_atempts']>=5 and data['login_date']==current_date:
                return jsonify({'status':False,'msg':'Too many Failed Login Attempts, Please retry after sometime...'})
            else:    
                db.resetpasswordattemptwithuname(uname)
                # otp = str(random.randint(100000,999999))
                otp = str(123456)
                print(otp)
                session['login_otp'] = otp
                return jsonify({'status':True,'msg':'Please Enter The OTP'}) 
        else:
            data=db.getloginattemptswithuname(uname)
            if data['login_atempts']>=5 and data['login_date']==current_date:
                    return jsonify({'status':False,'msg':'Too many Failed login Attempts, Please retry after sometime...'})
            db.failedlogin(uname)
            return jsonify({'status':False,'msg':'Incorrect Credentials...'}) 
        
# otp validation
def validate_otp():
    if request.method=='POST':
        uname = request.form['uname']
        passs = str(hashlib.md5(request.form['pass'].encode('UTF-8')).hexdigest())
        otp = str(request.form['otp'])
        current_date=getdatetime()
       
        if otp == session['login_otp']:
                data=db.checkuserlogin(uname,passs)

                if data['otp_atempts']>=5 and data['otp_date']==current_date:
                    return jsonify({'status':False,'msg':'Too many Failed OTP Attempts, Please retry after sometime...'})
                    
                session.pop('login_otp', None)
                db.resetotpattemptswithuname(uname)
                session['user_data']=data
                return jsonify({'status':True,'msg':'Login Successful','data':{ 'user_id': session['user_data']['user_id'], 'admin_name': session['admin_data']['admin_name'], 'admin_mobile': session['admin_data']['admin_mobile'], 'admin_email': session['admin_data']['admin_email'],'admin_role': session['admin_data']['admin_role']}})
        else:
            data=db.getotpattemptswithuname(uname)
            if data and data['otp_atempts']>=5 and data['otp_date']!=current_date:
                db.resetotpattemptswithuname(uname)
            if data:
                if data['otp_atempts']>=5 and data['otp_date']==current_date:
                    return jsonify({'status':False,'msg':'Too many Failed OTP Attempts, Please retry after sometime...'})
            db.failedOTP(current_date,uname)
            return jsonify({'status':False,'msg':'Incorrect Credentials...'})
        
# user logout
@api.route('/user_logout',methods=['POST','GET'])
def logout():
    if  'user_data' in session:
        session.pop('user_data', None)
        return jsonify({'status':True,'msg':"Logged out Successfully...."}) 
    else:
        return jsonify({'status':False,'msg':"Already Logged out...."})

# check session
@api.route('/getsession',methods=['POST','GET'])
def getsession():
    if 'user_data' in session: 
        print(session['admin_data'])
        return jsonify({'status':True,'data':{ 'admin_id': session['admin_data']['admin_id'], 'admin_name': session['admin_data']['admin_name'], 'admin_mobile': session['admin_data']['admin_mobile'], 'admin_email': session['admin_data']['admin_email'],'admin_role': session['admin_data']['admin_role']}})

    else:
        return jsonify({'status':False})

##### USERS #####

# added user by admin
@api.route('/add_user',methods=['POST'])
def insert():

    role = request.form['role']
    name = request.form['name']
    email = request.form['email']
    mobile = request.form['mobile']
    passs = str(hashlib.md5(request.form['passs'].encode('UTF-8')).hexdigest())
    # passs = request.form['passs']
    date = getdatetime()
    status = 1

    db.adduser(role,name,email,mobile,passs,date,status)

    return jsonify ({'status':True,'msg':'user added'})

# select single user added by admin
@api.route('/view_single_user', methods = ['POST'])
def viewsingleuser():

    idd = request.form['idd']

    data = db.viewsingleuser(idd)
    return jsonify ({'status':True, 'data':data, 'msg': 'single user details fetched'})

# select all users added by admin
@api.route('/view_all_users',methods = ['POST'])
def viewallusers():

    data = db.viewalluser()

    return jsonify ({'status':True, 'data':data, 'msg':'all users data fetched'})

# update users added by admin
@api.route('/update_users', methods = ['POST'])
def updateusers():

    role = request.form['role']
    name = request.form['name']
    email = request.form['email']
    mobile = request.form['mobile']
    idd = request.form['idd']

    db.updateuser(role, name, email, mobile, idd)
    return jsonify ({'status':True, 'msg': 'user updated'})

# deactivate user addded by admin
@api.route('/deactivate_user', methods = ['POST'])
def deactivateuser():

    idd = request.form['idd']
    db.deactivateuser(idd)
    return jsonify ({'status':True,'msg':'user deleted'})

##### PROJECTS #####

# add project
@api.route('/add_project', methods=['POST'])
def addproject():

    proj_name = request.form['proj_name']
    proj_desc = request.form['proj_desc']
    client_id = request.form['client_id']
    manager_id = request.form['manager_id']
    date = getdatetime()
    proj_images = uploadimage(request.files['proj_images'],'projects')
    proj_status = 1

    db.addproject(proj_name, proj_desc,client_id,manager_id,date,proj_images,proj_status)
    return jsonify ({'status':True,'msg':'project added successfully'})

# view all projects
@api.route('/view_projects', methods = ['POST'])
def viewprojets():

    data = db.viewallprojects()
    return jsonify ({'status': True, 'data': data,'msg': 'projects details fetched'})

# view single project
@api.route('/view_single_project', methods = ['POST'])
def viewsingleprojects():

    proj_id = request.form['proj_id']

    data = db.viewsingleproject(proj_id)
    return jsonify ({'status': True, 'data':data,'msg':'single project details fetched'})

# edit projects 
@api.route('/edit_projects', methods = ['POST'])
def editprojets():

    proj_name = request.form['proj_name']
    proj_desc = request.form['proj_desc']
    client_id = request.form['client_id']
    manager_id = request.form['manger_id'] 
    date = getdatetime()
    proj_images = uploadimage(request.files['proj_images'],'projects')
    proj_id = request.form['proj_id']

    db.editproject(proj_name, proj_desc, client_id, manager_id, date, proj_images, proj_id)
    return jsonify ({'status':True, 'msg':'projects updated'})

# delete project
@api.route('/delete_project', methods = ['POST'])
def deleteprojects():

    proj_id = request.form['proj_id']

    db.deleteproject(proj_id)
    return jsonify ({'status':True, 'msg':'project deactivated'})

##### SCOPES #####

# add scope 
@api.route('/add_scope', methods = ['POST'])
def addscope():

    proj_id = request.form['proj_id']
    manager_id = request.form['manager_id']
    client_id = request.form['client_id']
    scope_title = request.form['scope_title']
    scope_desc = request.form['scope_desc']
    scope_images = uploadimage(request.form['scope_images'],'scope')
    date = getdatetime()
    scope_approved = 0

    db.addscope(proj_id, manager_id, client_id, scope_title, scope_desc, scope_images, date, scope_approved)
    return jsonify ({'status':True, 'msg':'scope added'})

# view single scope
@api.route('/view_single_scope', methods = ['POST'])
def viewsinglescope():

    scope_id = request.form['scope_id']

    data = db.viewsinglescope(scope_id)
    return jsonify ({'status': True, 'msg': 'single scope details fetched'})

# view approved scopes
@api.route('/view_approved_scope', methods = ['POST'])
def viewapprovedscope():

    db.viewallapprovedscopes()
    return jsonify ({'status':True, 'msg':'approved scope details fetched'})

# view all scopes
@api.route('/view_all_scopes', methods =['POST'])
def viewallscopes():

    db.viewallscopes()
    return jsonify ({'status':True, 'msg':'scope details fetched'})

# edit scope
@api.route('/edit_scope', methods = ['POST'])
def editscope():

    db.editscope()
    return jsonify ({'staus':True, 'msg':'scope updated'})

# approve scope
@api.route('/approve_scope', methods=['POST'])
def approvescope():

    scope_id = request.form['scope_id']
    db.approvescope(scope_id)
    
    return jsonify ({'status':True, 'msg': 'scope approved'})

# delete scope
@api.route('/delete_scope', methods = ['POST'])
def deletescope():

    scope_id = request.form['scope_id']
    db.deletescope(scope_id)
    
    return jsonify ({'status':True, 'msg':'scope deactivatd'})

##### TASKS #####

# add tasks
@api.route('/add_task', methods = ['POST'])
def addtask():

    proj_id = request.form['proj_id']
    scope_id = request.form['scope_id']
    task_title = request.form['task_title']
    task_desc = request.form['task_desc']
    assigned_by = request.form['task_assigned_by']
    assigned_to = request.form['task_assigned_to']
    created_date = getdatetime()
    due_date = request.form['due_date']
    task_image = uploadimage(request.form['task_image'],'tasks')
    task_status = 1

    db.addtasks(proj_id, scope_id, task_title, task_desc, assigned_by, assigned_to, created_date, due_date, task_image, task_status)
    return jsonify ({'status':True, 'msg':'task added'})

# view single task
@api.route('/view_single_task', methods = ['POST'])
def viewsingletask():

    task_id = request.form['task_id']

    data = db.viewsingletask(task_id)
    return jsonify ({'staus':True, 'data':data, 'msg':'single task details fetched'})

# view all tasks
@api.route('/view_all_tasks', methods= ['POST'])
def viewalltasks():

    data = db.viewalltasks()
    return jsonify ({'staus':True, 'data':data, 'msg': 'all task details fetched'})

# edit tasks
@api.route('/edit_tasks', methods=['POST'])
def edittasks():

    proj_id = request.form['proj_id']
    scope_id = request.form['scope_id']
    task_title = request.form['task_tiile']
    task_desc = request.form['task_desc']
    assigned_by = request.form['assigned_by']
    assigned_to = request.form['assigned_to']
    due_date = request.form['due_date']
    task_images = uploadimage(request.form['images'],'tasks')
    task_id = request.form['task_id']

    db.edittask(proj_id, scope_id, task_title, task_desc, assigned_by, assigned_to,due_date, task_images,task_id)
    return jsonify ({'status':True, 'msg':'task updated'})

# delete task
@api.route('/delete_task', methods = ['POST'])
def deletetask():

    task_id = request.form['task_id']

    db.deletetask(task_id)
    return jsonify ({'status':True, 'msg':'task deactivated'})