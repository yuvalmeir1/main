#region    info
# trade.py
# path C:\Users\User\PycharmProjects\vsProject\anconda\mq5_py\trade.py
# web url for fix  the timed out exception https://www.py4u.net/discuss/141668
# this app link https://www.mql5.com/en/docs/integration/python_metatrader5/mt5accountinfo_py
# link to functions https://www.mql5.com/en/docs/integration/python_metatrader5/mt5copyratesfrom_py

#endregion

from datetime import datetime
import time
import MetaTrader5 as mt
import pandas as pd
# from datetime  import datet
import plotly.express  as px
import sys
import MetaTrader5 as mt5
import sqlite3
class xcel_class():
    def __init__(self,filname):
        self.filname=filname

    def read_book_pandas(self):
        df =pd.read_excel(self.filname)
        res2=df.iloc[10,1:16]
        print (res2)

        res3=res2.dropna()        
        print (res3)

        res3.index = ['symbol', 'volume', 'buy/sell', 'profit_method', 'p_method_val', 'loss_method', 'l_method_val','ok for trade']      
        print (res3)

        res3.columns =['value',]
        print(res3)
        return res3

class  sqlACCESS:
#      """sqlite3 database class that holds testers jobs"""
    # DB_LOCATION = "/root/Documents/testerJobSearch/tester_db.sqlite"

    def __init__(self,dbpath):
        self.dbpath=dbpath
        # self.symbol=symbol

    def connect(self):

        try:
            connection=""
            connection = sqlite3.connect(self.dbpath)
            cursr=connection.cursor()
            comand=''' CREATE TABLE IF NOT EXISTS 
            PAIRS (pair STRING PRIMARY KEY,toggle INTEGER ) '''
            cursr.execute(comand)
            return connection

        except sqlite3.Error as error:
            print (error)
            return ""

class sqlUPDATE (sqlACCESS):
    def __init__(self, dbpath,symbol):  # time satmp 8:30
        super().__init__(dbpath)
        self.dbpath=dbpath
        self.symbol=symbol
        error=""

    def check_status(self,symbol):
        connection=self.connect()
        if connection=="":
           return

        t_oggle = self.find(symbol,connection) 
        return t_oggle

    def change_toggle (self,symbol,toggle) :
        connection=self.connect()  
        if connection=="":
            return

        cursr=connection.cursor()
        #error="caused by update"
        try:
            #cursr.execute("SELECT * FROM PAIRS WHERE pair=?", (symbol,))
            #error="pair not found"
            #toggle=cursr.fetchone()[1]
            #error=""

            print ("in togle =",toggle)

            #if toggle==1:
            #    toggle=0
            #else:
            #    toggle=1

            toggle=0;

            #print ("out toggle ",toggle)

            error="update error"
            cursr.execute("Update PAIRS set toggle = ? where pair = ?", (toggle,symbol,))
            connection.commit()
            error="Record Updated successfully "
        except sqlite3.Error as e:
            print (error)
        finally:

            print (error)
            return

    def find (self,symbol,connection) :
        error="PAIR NOT FOUND"
        try:
            cursr=connection.cursor()
            cursr.execute("SELECT * FROM PAIRS WHERE pair=?", (symbol,))
            error="TOGGLE ERROR"
            toggle=cursr.fetchone()[1]
            error=""
            
        except sqlite3.Error as e:
            print (error)
        finally:

            print (error)
            print ("in togle =",toggle)
            return toggle

class accnt:
    def __init__(self,login, passwd , account ):
        self.login=login
        self.passwd=passwd
        self.account=account

    def account_info(self):
        error="initialize"
        try:
            mt.initialize()
            error="login"
            authorized = mt.login( self.login,self.passwd,self.account)
            error=""
        except Exception as e:
            print (e)
        finally:
            print (error)
            return

    def terminal_info(self):
        mt.initialize()
        #print ( mt5.terminal_info())
        return  mt5.terminal_info()


    def terminal_info_df(self):         
    # web example https://www.mql5.com/en/docs/integration/python_metatrader5/mt5accountinfo_py
         account_info_dict = mt5.account_info()._asdict()
         df=pd.DataFrame(list(account_info_dict.items()),columns=['property','value'])
         print(df)


    def terminal_info_dict(self):
        account_info_dict = mt5.account_info()._asdict()
        for prop in account_info_dict:
            print("  {}={}".format(prop, account_info_dict[prop]))
        print()

class currency:
    def __init__(self,symbol):
        self.symbol=symbol

    def symbol_info(self):
        #return mt5.symbol_info(self.symbol)
        sym_dict =mt5.symbol_info(self.symbol)._asdict()
        print (sym_dict)
        df_sym=pd.DataFrame(list(sym_dict.items()),columns=['property','value'])
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        print (df_sym)



class trade (accnt) :
    def __init__(self,login, passwd , account ,symbol):
        super().__init__(login, passwd , account )
        self.symbol=symbol 

    def buy_order (self) :        
        self.account_info()
        
        requst={
                'action': mt.TRADE_ACTION_DEAL,
                'symbol':self.symbol,
                'volume' :0.01, 
                'type':  mt.ORDER_TYPE_BUY,
                'price' : mt.symbol_info_tick(self.symbol).ask,
                'sl' : 0.0,
                'tp' : 0.0 ,
                'deviation' : 20 ,
                'magic' : 23400 ,
                'comment' : 'py scritpt order',
                'type_time' : mt.ORDER_TIME_GTC,
                'type_fillint' : mt.ORDER_FILLING_IOC
        }
        order=mt.order_send(requst)
        ret_code=order.retcode
        if ret_code==10009:
            print ('-------------->  BUY ORDER OK ',symbol)
            print(order)
        else :
            print ('-------------->  BUY ORDER FAILED  ',ret_code,"   ",symbol )

        
    def sell_order (self) :        
        self.account_info()
        
        requst={
                'action': mt.TRADE_ACTION_DEAL,
                'symbol':self.symbol,
                'volume' :0.01, 
                'type':  mt.ORDER_TYPE_SELL,
                'price' : mt.symbol_info_tick(self.symbol).ask,
                'sl' : 0.0,
                'tp' : 0.0 ,
                'deviation' : 20 ,
                'magic' : 23400 ,
                'comment' : 'py scritpt order',
                'type_time' : mt.ORDER_TIME_GTC,
                'type_fillint' : mt.ORDER_FILLING_IOC
        }
        order=mt.order_send(requst)
        ret_code=order.retcode
        if ret_code==10009:
            print ('-------------->  SELL ORDER OK ',symbol)
            print(order)
        else :
            print ('-------------->  SELL ORDER FAILED  ',ret_code,"  ",symbol)

#--------------------------------------------------------

xcel=xcel_class('C:\\MyapS\\forex\\Excels\\parms_TRADE.xlsm')

res3=xcel.read_book_pandas()
symbol=res3.iloc[0]
volume=res3.iloc[1] # first five rows of dataframe

acc = accnt(681011,'xQ7c932$Pm','IFCMarkets-Demo')

acc.terminal_info()
acc.terminal_info_df()
#acc.terminal_info_dict()

sym=currency(symbol)
sym.symbol_info()

dbpath=(r"C:\Users\User\Desktop\STUDENTS.db")
#symbol = 'EURUSD'

sqlB = sqlUPDATE(dbpath,symbol);

order=trade(681011,'xQ7c932$Pm','IFCMarkets-Demo',symbol)

n=1
while n>0:
    toggle = sqlB.check_status(symbol)
    if toggle==10:
        order.buy_order()
        sqlB.change_toggle(symbol,toggle)
    elif toggle==11:
        order.sell_order()
        sqlB.change_toggle(symbol,toggle)

    time.sleep(180) # Sleep  3 minutes

input ('')
