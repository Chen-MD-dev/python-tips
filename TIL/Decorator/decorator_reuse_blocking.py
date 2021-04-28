# -*- coding: utf-8 -*-

def handler(qry_function):
    db_con = "db~~"
    db_cursor = "session"
    print db_con, db_cursor
    def wrapper(db_qry):
        print db_qry
        return True
    return wrapper

@handler
def db_qry(qry):
    return qry

for i in range(0, 10):
    db_qry('select * from table_name')
