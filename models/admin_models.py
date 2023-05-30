from extensions import mysql


class models:

##### LOGIN VALIDATIONS ######

    # check user login
    def checkuserlogin(uname, passs):
        cur = mysql.connection.cursor()
        sql = "SELECT `user_id`, `user_role`, `user_name`, `user_email`, `user_mobile`, `user_pass`, `reg_date`, `user_status` FROM `users` WHERE (`user_email` = %s or `user_mobile` = %s) and `user_pass` = %s and `user_status = 1"
        cur.execute(sql,[uname,uname,passs])
        data = cur.fetchall()
        cur.close()
        return data
    
    # reset password attempts with uname
    def resetpasswordattemptwithuname(uname):
        cur = mysql.connection.cursor()
        sql ="UPDATE `users` SET `login_attempts`= 0 WHERE `user_email` = %s or `user_mobile` = %s"
        cur.execute(sql,[uname,uname])
        mysql.connection.commit()
        cur.close()

    # getloginattemptswithuname
    def getloginattemptswithuname(uname):
        cur = mysql.connection.cursor()
        sql ="SELECT `user_id`, `user_role`, `user_name`, `user_email`, `user_mobile`, `user_pass`, `reg_date`, `login_attempts`, `user_status` FROM `users` WHERE `user_email` = %s or `user_mobile` = %s"
        cur.execute(sql,[uname,uname])
        data = cur.fetchone()
        cur.close()
        return data
    
    # failed login
    def failedlogin(uname):
        cur = mysql.coneection.cursor()
        sql = "UPDATE `users` SET `login_attempts`= `login_attempts`+1  WHERE `user_email` = %s or `user_mobile` = %s"
        cur.execute(sql,[uname, uname])
        mysql.connection.commit()
        cur.close()

    # reset otp attempts with uname
    def resetotpattemptswithuname(uname):
        cur = mysql.connection.cursor()
        sql = "SELECT `user_id`, `user_role`, `user_name`, `user_email`, `user_mobile`, `user_pass`, `reg_date`, `login_attempts`, `user_status` FROM `users` WHERE `user_email` = %s or `user_mobile` = %s and `user_status` = 1"
        cur.execute(sql,[uname,uname])
        data = cur.fetchone()
        cur.close()
        return data
    
    # get otp attempts with uname
    def getotpattemptswithuname(uname):
        cur = mysql.connection.cursor()
        sql = "SELECT `user_id`, `user_role`, `user_name`, `user_email`, `user_mobile`, `user_pass`, `reg_date`, `login_attempts`, `user_status` FROM `users` WHERE `user_email` = %s or `user_mobile` = %s and `user_status` = 1"
        cur.execute(sql,[uname,uname])
        data = cur.fetchone()
        cur.close()
        return data
    
    # failed otp
    def failedotp(uname):
        cur = mysql.connection.cursor()
        sql = "UPDATE `users` SET `otp_attempts`=`otp_attempts`+1 WHERE `user_email` = %s or `user_mobile` = %s and `user_status` = 1"
        cur.execute(sql,[uname,uname])
        mysql.connection.commit()
        cur.close()


##### USERS #####

    # user added by admin
    def adduser(role, name, email, mobile, passs, regdate, status):
        cur = mysql.connection.cursor()
        sql ="INSERT INTO `users`(`user_role`, `user_name`, `user_email`, `user_mobile`, `user_pass`, `reg_date`, `user_status`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql,[role, name, email, mobile, passs, regdate, status])
        mysql.connection.commit()
        cur.close()

    # view single user added by admin to edit
    def viewsingleuser(idd):
        cur = mysql.connection.cursor()
        sql = "SELECT `user_id`, `user_role`, `user_name`, `user_email`, `user_mobile`, `user_pass`, `reg_date`, `user_status` FROM `users` WHERE `user_id` = %s"
        cur.execute(sql,[idd])
        data = cur.fetchone()
        cur.close()
        return data

    # view all users added by admin
    def viewalluser():
        cur = mysql.connextion.cursor()
        sql = "SELECT `user_id`, `user_role`, `user_name`, `user_email`, `user_mobile`, `user_pass`, `reg_date`, `user_status` FROM `users` WHERE `user_status`= 1;"
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        return data

    # update user added admin
    def updateuser(role, name, email, mobile, idd):
        cur = mysql.connection.cursor()
        sql = "UPDATE `users` SET `user_role`= %s,`user_name`= %s,`user_email`= %s,`user_mobile`= %s WHERE `user_id`= %s;"
        cur.execute(sql,[role, name, email, mobile, idd])
        mysql.connection.commit()
        cur.close()

    # delete user added by admin
    def deactivateuser(idd):
        cur = mysql.connection.cursor()
        sql = "UPDATE `users` SET `user_status`= 0 WHERE `user_id`= %s;"
        cur.execute(sql,[idd])
        mysql.connection.commit()
        cur.close()

##### PROJECTS #####

    # add project by admin/manager
    def addproject(proj_name, proj_desc, client_id, manager_id, date, proj_images, proj_status):
        cur = mysql.connection.cursor()
        sql = "INSERT INTO `project`(`project_name`, `project_desc`, `client_id`, `manager_id`, `created_date`, `project_images`, `project_status`) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(sql,[proj_name, proj_desc, client_id, manager_id, date, proj_images,proj_status])
        mysql.connection.commit()
        cur.close()

    # view single project to edit
    def viewsingleproject(proj_id):
        cur = mysql.connection.cursor()
        sql = "SELECT `project_id`, `project_name`, `project_desc`, `client_id`, `manager_id`, `created_date`, `project_images` FROM `project` WHERE `project_id` = %s"
        cur.execute(sql,[proj_id])
        data = cur.fetchone()
        cur.close()
        return data
    
    # view all projects
    def viewallprojects():
        cur = mysql.connection.cursor()
        sql = "SELECT `project_id`, `project_name`, `project_desc`, `client_id`, `manager_id`, `created_date`, `project_images` FROM `project` WHERE `project_status`= 1;"
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        return data

    # edit project
    def editproject(proj_name, proj_desc, client_id, manager_id, date, proj_images, proj_id):
        cur = mysql.connection.cursor()
        sql = "UPDATE `project` SET `project_name`= %s,`project_desc`= %s,`client_id`= %s,`manager_id`= %s,`created_date`= %s,`project_images`= %s WHERE `project_id` = %s"
        cur.execute(sql,[proj_name, proj_desc, client_id, manager_id, date, proj_images, proj_id])
        mysql.connection.commit()
        cur.close()

    # delete project
    def deleteproject(proj_id):
        cur =  mysql.connection.cursor()
        sql = "UPDATE `project` SET `project_status`= 0 WHERE `project_id` = %s"
        cur.execute(sql,[proj_id])
        mysql.connection.commit()
        cur.close()

##### SCOPES #####

    # add scopes
    def addscope(proj_id, manager_id, client_id, scope_title, scope_desc, scope_images, date, scope_approved):
        cur = mysql.connection.cursor()
        sql = "INSERT INTO `scopes`(`project_id`, `manager_id`, `client_id`, `scope_title`, `scope_desc`, `scope_images`, `created_date`, `scope_approved`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)`"
        cur.execute(sql,[proj_id, manager_id, client_id, scope_title, scope_desc, scope_images, date, scope_approved])
        mysql.connection.commit()
        cur.close()

    # view single scopes
    def viewsinglescope(scope_id):
        cur = mysql.connection.cursor()
        sql = "SELECT `scope_id`, `project_id`, `manager_id`, `client_id`, `scope_title`, `scope_desc`, `scope_images`, `created_date`, `scope_approved` FROM `scopes` WHERE `scope_id` = %s"
        cur.execute(sql,[scope_id])
        data = cur.fetchone()
        cur.close()
        return data
    
    # view all approves scopes
    def viewallapprovedscopes():
        cur = mysql.connection.cursor()
        sql = "SELECT `scope_id`, `project_id`, `manager_id`, `client_id`, `scope_title`, `scope_desc`, `scope_images`, `created_date`, `scope_approved` FROM `scopes` WHERE `scope_approved` = 1"
        cur.execute(sql)
        data = cur.fectchall()
        cur.close()
        return data
    
    # view all scopes
    def viewallscopes():
        cur = mysql.connection.cursor()
        sql = "SELECT `scope_id`, `project_id`, `manager_id`, `client_id`, `scope_title`, `scope_desc`, `scope_images`, `created_date`, `scope_approved` FROM `scopes` WHERE 1"
        cur.execute(sql)
        data = cur.fectchall()
        cur.close()
        return data
    
    # edit scope
    def editscope():
        cur = mysql.connection.cursor()
        sql = "UPDATE `scopes` SET `project_id`='[value-2]',`manager_id`='[value-3]',`client_id`='[value-4]',`scope_title`='[value-5]',`scope_desc`='[value-6]',`scope_images`='[value-7]',`created_date`='[value-8]' WHERE `scope_id`= %s"
        cur.execute(sql)
        mysql.connection.commit()
        cur.close()

    # approve scope
    def approvescope(scope_id):
        cur = mysql.connection.cursor()
        sql = "UPDATE `scopes` SET ,`scope_approved`= 1 WHERE `scope_id` = %s;"
        cur.execute(sql,[scope_id])
        mysql.connection.commit()
        cur.close()

    # delete scope
    def deletescope(scope_id):
        cur =  mysql.connection.cursor()
        sql = "UPDATE `scopes` SET `scope_approved`= 0 WHERE `scope_id` = %s"
        cur.execute(sql,[scope_id])
        mysql.connection.commit()
        cur.close()

##### TASKS #####

    # add task
    def addtasks(proj_id, scope_id, task_title, task_desc, task_assigned_by, task_assigned_to, created_date, due_date, task_images, task_status):
        cur = mysql.connection.cursor()
        sql = "INSERT INTO `tasks`(`project_id`, `scope_id`, `task_title`, `task_desc`, `task_assigned_by`, `task_assigned_to`, `task_created_date`, `task_due_date`, `task_images`, `task_status`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql, [proj_id, scope_id, task_title, task_desc, task_assigned_by, task_assigned_to, created_date, due_date, task_images, task_status])
        mysql.connection.commit()
        cur.close()

    # view single task
    def viewsingletask(task_id):
        cur = mysql.connection.cusor()
        sql = "SELECT `task_id`, `project_id`, `scope_id`, `task_title`, `task_desc`, `task_assigned_by`, `task_assigned_to`, `task_created_date`, `task_due_date`, `task_images`, `task_status` FROM `tasks` WHERE `task_id` = %s"
        cur.execute(sql, [task_id])
        data = cur.fechone()
        cur.close()
        return data

    # view all tasks
    def viewalltasks():
        cur = mysql.connection.cursor()
        sql = "SELECT `task_id`, `project_id`, `scope_id`, `task_title`, `task_desc`, `task_assigned_by`, `task_assigned_to`, `task_created_date`, `task_due_date`, `task_images`, `task_status` FROM `tasks` WHERE 1"
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        return data
    
    # edit task
    def edittask(proj_id, scope_id, task_title, task_desc, assigned_by, assigned_to, due_date, task_images, task_id):
        cur = mysql.connection.cursor()
        sql =  "UPDATE `tasks` SET `project_id`= %s,`scope_id`= %s,`task_title`= %s,`task_desc`= %s,`task_assigned_by`= %s,`task_assigned_to`= %s,`task_due_date`= %s,`task_images`= %s WHERE `task_id` = %s"
        cur.execute(sql, [proj_id, scope_id, task_title, task_desc, assigned_by, assigned_to, due_date, task_images, task_id ])
        mysql.connection.commit()
        cur.close()

    # delete task
    def deletetask(task_id):
        cur = mysql.connection.cursor()
        sql = "UPDATE `tasks` SET `task_status`= 0 WHERE `task_id` = %s;"
        cur.execute(sql,[task_id])
        mysql.connection.commit()
        cur.close()