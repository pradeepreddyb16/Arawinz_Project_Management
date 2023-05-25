from extensions import mysql


class models:
    
    def addtask():
        cur = mysql.coneection.cursor()
        sql =""
        cur.execute(sql)
        mysql.connection.commit()
        cur.close()


    