import sqlite3

def initDb():
    with sqlite3.connect("financial.db") as conn:
        cursor=conn.cursor()
        cursor.execute('create table IF NOT EXISTS fund (id integer primary key autoincrement,code varchar(20) unique,name varchar(20),state int default 0)')
        cursor.execute('''create table IF NOT EXISTS fund_hist(id integer primary key autoincrement,code varchar(20),
        FSRQ varchar(20),DWJZ varchar(10),LJJZ varchar(10),
        SDATE varchar(20),ActualSYI varchar(10),NAVTYPE varchar(10),
        JZZZL varchar(10),SGZT varchar(20),SHZT varchar(20),
        FHFCZ varchar(20),FHFCBZ varchar(20),DTYPE varchar(10),
        FHSP varchar(20))
        ''')
        cursor.close()
def insertData(fund):
    with sqlite3.connect("financial.db") as conn:
        cursor=conn.cursor()
        cursor.execute("insert or ignore into fund(code,name) values('{0}','{1}')".format(fund['code'],fund['name']))
        cursor.close()
        conn.commit()
def insertList(funds):
    with sqlite3.connect("financial.db") as conn:
        cursor=conn.cursor()
        for fund in funds:
            cursor.execute("insert or ignore into fund(code,name) values('{0}','{1}')".format(fund['code'],fund['name']))
        cursor.close()
        conn.commit()
def getList():
    result=None
    with sqlite3.connect("financial.db") as conn:
        cursor=conn.cursor()
        cursor.execute("select * from fund")
        result=cursor.fetchall()
        cursor.close()
    return result
def delete():
    with sqlite3.connect("financial.db") as conn:
        cursor=conn.cursor()
        cursor.execute("delete from fund")
        cursor.close()
        conn.commit()      


def insertHistList(hists):
    sql='''insert or ignore into fund_hist(code,FSRQ,DWJZ,LJJZ,
            SDATE,ACTUALSYI,NAVTYPE,JZZZL,SGZT,SHZT,FHFCZ,FHFCBZ,DTYPE,
            FHSP) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    with sqlite3.connect("financial.db") as conn:
        conn.executemany(sql,hists)
        conn.commit()

def clear(tableName):
    with sqlite3.connect("financial.db") as conn:
        cursor=conn.cursor()
        cursor.execute("delete from {0}".format(tableName))
        cursor.close()
        conn.commit() 
    