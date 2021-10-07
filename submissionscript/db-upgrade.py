import sys
import mysql.connector
import json
import glob
import re
from itertools import takewhile

list_sql_files=[]
db_connection=''
db_cursor=''

db_connection = mysql.connector.connect(
user=sys.argv[2],
host=sys.argv[3],
passwd=sys.argv[5],
database=sys.argv[4]
)

db_cursor = db_connection.cursor(dictionary=True)

print("first step")
print(db_cursor)


def update_table_version(new_number):
    db_cursor.execute("UPDATE versionTable SET version="+"'"+str(new_number)+"'"+";")
    db_connection.commit()
    Res = db_cursor.fetchone()
    print(Res)
#update_table_version(4)

def get_current_version():
    db_cursor.execute("SELECT version FROM versionTable;")
    data=db_cursor.fetchone()
    return data["version"]
#print(get_current_version())


def prefix_sql_file(sql_file):
    return ''.join(takewhile(str.isdigit,sql_file)).lstrip('0')

#print(str(prefix_sql_file("045  uuuuu.sql")))

def execution_sql_files(sqlfolder,current_db_version):
    global list_sql_files
    list_sql_files=glob.glob(sqlfolder+"/"+"[0-9]*.sql")
    
    print("folder in="+sqlfolder)

    print("list before sort "+ str(list_sql_files))

    list_sql_files.sort(key=lambda test_string : list(map(int, re.findall(r'\d+', test_string)))[0])   
    
    print("list after sort "+ str(list_sql_files))
    print("current_db_version="+str(current_db_version))
   
    for current_file in list_sql_files:
        print("CURRENTFILE="+current_file)
        current_file=current_file.replace(sqlfolder+"/",'')
        print("PREFIX="+prefix_sql_file(current_file))
        if current_db_version < int(float(prefix_sql_file(current_file))): 
            update_table_version(int(float(prefix_sql_file(current_file))))
            print("UPDATE SQL EXECUTED")

execution_sql_files(sys.argv[1],get_current_version())
        
                      




