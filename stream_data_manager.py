import os
import mysql.connector as msc
from time import sleep
from threading import Thread

home = os.getcwd()

stage1_flag = 0
stage2_flag = 0

dirs = ['processing', 'queue', 'processed']

for dir in dirs:
    os.mkdir(home + '\\' + dir)
    
mydb = msc.connect(
    host = "localhost",
    user = "minmay",
    password = "password"
    )


cursor0 = mydb.cursor()
cursor0.execute("CREATE DATABASE IF NOT EXISTS proc_db")
cursor0.execute("USE proc_db")
cursor0.execute("""CREATE TABLE IF NOT EXISTS proc_status (
    filename VARCHAR(255),
    current_status INT
    )
    """)


class file_creator(Thread):
    def run(self):
        global stage1_flag
        for file in range(100):
            name ='file_'+str(file)+'.txt'
            with open(home + '\\' + dirs[0] + '\\' + name,'w') as newfile:
                pass
            newfile.close()
            cursor1 = mydb.cursor()
            cursor1.execute('USE proc_db')
            cursor1.execute("INSERT INTO proc_status (filename, current_status) VALUES ('"+ name  +"',0)")
            mydb.commit()
            cursor1.close()
            sleep(1)
        stage1_flag = 1


class stage1_move(Thread):
    def run(self):
        global stage1_flag
        global stage2_flag
        while stage1_flag == 0:
            queuef_list = os.listdir(home + '\\' + dirs[1])
            processingf_list = os.listdir(home + '\\' + dirs[0])
            if len(queuef_list) == 0:
                for file in processingf_list:
                    os.replace(home + '\\' + dirs[0] + '\\' + file, home + '\\' + dirs[1] + '\\' + file )
                sleep(5)
        stage2_flag = 1

class stage2_move(Thread):
    def run(self):
        global stage2_flag
        while stage2_flag == 0:
            queuef_list = os.listdir(home + '\\' + dirs[1])
            for file in queuef_list:
                os.replace(home + '\\' + dirs[1] + '\\' + file, home + '\\' + dirs[2] + '\\' + file )
                cursor2 = mydb.cursor()
                cursor2.execute("USE proc_db")
                cursor2.execute ("""
                                    UPDATE proc_status
                                    SET current_status=%s
                                    WHERE filename=%s
                                    """, ("1", file))
                mydb.commit()
                cursor2.close()

task1 = file_creator()
task2 = stage1_move()
task3 = stage2_move()

task1.start()
#sleep(0.2)
task2.start()
#sleep(0.2)
task3.start()

task1.join()
task2.join()
task3.join()

cursor0.close()
mydb.close()


            
