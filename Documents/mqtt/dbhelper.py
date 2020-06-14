import pandas as pd
import mysql.connector


import dbconfig

def floatInf0(fstr):
    fres = float(fstr)
    if np.isinf(fres):
        fres = 0
    return fres

class DBHelper:
    def __init__(self, host='127.0.0.1'):
        dbconfig.setHost(host)

    def connect(self):
        #print ("Getting connection to database")
        return mysql.connector.connect(
            host=dbconfig.db_host, 
            user=dbconfig.db_user, 
            password=dbconfig.db_password,
            database=dbconfig.db_name)

    def insertStatusRec(self, tim, dat):
        conn = self.connect()
        try:
            query1 = """insert cputemp_table 
            (temp_time, temp_data)
            values (%s, %s); """
            cursor = conn.cursor()
            
            cursor.execute(query1, (tim, dat))
                
            conn.commit()    
            
        except Exception as e:
            print("DB Error at insertStatusRec", e)
        finally:
            conn.close()

    def insertStatusRecList(self, recList):
        conn = self.connect()
        try:
            query1 = """insert resp_table 
            (dev_id, rec_time, resp_data)
            values (%s, %s); """
            cursor = conn.cursor()
            
            for rec in recList:
                tim = rec['rec_time']
                dat = rec['resp_data']
                cursor.execute(query1, (tim, dat))
                
            conn.commit()    
            
        except Exception as e:
            print("DB Error at insertStatusRec", e)
        finally:
            conn.close()

    def buildStatusDFFromDB(self, num=None):
        conn = self.connect()
        cursor = conn.cursor()
        
        
        df_data = {'time':[], 'Temp':[], 'CPU':[], 'Mem':[]}
        query = "select temp_time, temp_data from cputemp_table "
        cursor.execute(query)
        for row in cursor:
            item = row[1].split(',')
            df_data['time'].append(row[0].strftime("%M:%S"))
            df_data['Temp'].append(float(item[0]))
            df_data['CPU'].append(float(item[1])) 
            df_data['Mem'].append(float(item[3])) 
        
        statdf = pd.DataFrame(data=df_data)
        statdf = statdf.set_index('time')
        if num is None:
            return statdf
        statdf = statdf.tail(num)
        return statdf
        
