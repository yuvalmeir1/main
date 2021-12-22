# trade.py
# path C:\Users\User\PycharmProjects\vsProject\anconda\mq5_py\trade.py
# web url for fix  the timed out exception https://www.py4u.net/discuss/141668
# this app link https://www.mql5.com/en/docs/integration/python_metatrader5/mt5accountInfo_py
# link to functions https://www.mql5.com/en/docs/integration/python_metatrader5/mt5copyratesfrom_py
# DDDDDDDDDDDDDDDDDDDDDDDDDhhhhhhhhhhhhhhhhhhhhhh
import time
import MetaTrader5 as mt5
import sqlite3

import pandas as pd
import sys


class getExcel:
    def __init__(self, filname):
        self.filname = filname

    def read_book_pandas(self):
        error = "FAILED TO OPEN EXCEL FILE"
        try:
            df = pd.read_excel(self.filname)
            error = "FAILED TO LOC DATA LINE "
            res1 = df.iloc[10, 1:16]

            res2 = res1.dropna()

            error = "FAILED TO ASSIGN INDEX"
            res2.index = ['symbol', 'volume', 'buy/sell', 'profit_method', 'p_method_val', 'loss_method',
                          'l_method_val', 'ok for trade']
            return res2
        except Exception as e:
            print(e)
            print(error)


class sqlAccess:
    def __init__(self, dbpath):
        self.dbpath = dbpath
        # self.symbol=symbol

    def connect(self):

        try:
            connection = sqlite3.connect(self.dbpath)
            cursr = connection.cursor()
            comand = ''' CREATE TABLE IF NOT EXISTS 
            PAIRS (pair STRING PRIMARY KEY,toggle INTEGER ) '''
            cursr.execute(comand)
            return connection

        except sqlite3.Error as error:
            print(error)
            return ""


class sqlUdate:
    connection = None
    cursr = None

    def __init__(self, dbpath):  # time satmp 8:30
        #        def __init__(self, dbpath,symbol):  # time satmp 8:30
        self.dbpath = dbpath

    def connect(self):
        error = "CONNECT FAILED "
        try:
            self.connection = sqlite3.connect(self.dbpath)
            self.cursr = self.connection.cursor()
            error = "TABLE  FAILED "
            comand = ''' CREATE TABLE IF NOT EXISTS 
            PAIRS (pair STRING PRIMARY KEY,toggle INTEGER ) '''
            self.cursr.execute(comand)
            return self.connection

        except sqlite3.Error as e:
            print(e)
            print(error)

    def check_status(self):
        if self.connection is None:
            return

    def change_toggle(self, symbol, toggle):
        error = ""
        try:
            error = "UPDATE ERROR"
            self.cursr.execute("Update PAIRS set toggle = ? where pair = ?", (toggle, symbol,))
            error = "COMMIT FAILED"
            self.connection.commit()
            error = ""
            print("RECORD UPDATED SUCCESSFULLY ")
        except sqlite3.Error as e:
            print(e)
            print(error)

    def find(self, symbol):

        error = "PAIR NOT FOUND"
        try:
            self.cursr.execute("SELECT * FROM PAIRS WHERE pair=?", (symbol,))
            error = "TOGGLE ERROR"
            error = ""

        except sqlite3.Error as e:
            print(e)
            print(error)

    def read_sequntial(self):
        """
        web https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/
        """
        if self.connection is None:
            sys.exit(0)
        if self.cursr is None:
            sys.exit(0)

        # cursr=connection.cursor()
        error = "FAILED TO SELECT ROWS"
        try:
            self.cursr.execute("SELECT * FROM pairs")
            error = "FAILED TO FETCH ROWS"
            rows = self.cursr.fetchall()
            return rows
        except sqlite3.Error as e:
            print(e)
            print(error)


class accountInfo:
    authorized = False
    acc_info = None

    def __init__(self, login, passwd, account):
        self.login = login
        self.passwd = passwd
        self.account = account

    #   ---------- account  data
    def account_info(self):
        error = "FAILED INITIALIZE"
        try:
            mt5.initialize()
            error = "FAILED LOGIN"
            self.authorized = mt5.login(self.login, self.passwd, self.account)
            error = ""
        except Exception as e:
            print(e)
            print(error)

        if self.authorized:
            return mt5.account_info()

    #   ---------- terminal  data
    def terminal_data(self):
        if self.authorized:
            account_info_dict = mt5.account_info()._asdict()
            return account_info_dict

    # url https://www.mql5.com/en/docs/integration/python_metatrader5/mt5accountInfo_py
    def terminal_info_df(self):
        if self.authorized:
            account_info_dict = mt5.account_info()._asdict()
            df = pd.DataFrame(list(account_info_dict.items()), columns=['property', 'value'])
            return df

    def terminal_info(self):
        if self.authorized:
            return mt5.terminal_info()


class symbolIno:
    def __init__(self, symbol, b_s):
        self.symbol = symbol
        self.b_s = b_s

    def symbol_data(self):
        # return mt5.symbol_info(self.symbol)
        sym_dict = mt5.symbol_info(self.symbol)._asdict()
        print(sym_dict)
        df_sym = pd.DataFrame(list(sym_dict.items()), columns=['property', 'value'])
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        print(df_sym)

        symbol_values = mt5.symbol_info(self.symbol)
        if self.b_s == 0:  # buy ask
            return symbol_values.ask
        else:  # sell bid
            return symbol_values.bid


class sendOrder(accountInfo):

    def __init__(self, login, passwd, account, symbol):
        super().__init__(login, passwd, account)
        self.symbol = symbol

    def send_order(self, pair, s_b):
        error = ""
        order_price = 0
        try:
            if s_b == 0:
                order_price = mt5.symbol_info_tick(pair).ask
            else:
                order_price = mt5.symbol_info_tick(pair).bid
        except Exception as e:
            print(e)
            error = "SYMBOL NOT FOUND  "
        finally:
            if error != "":
                print(error, pair)
                return 0

        self.account_info()

        requst = {
            'action': mt5.TRADE_ACTION_DEAL,
            # 'symbol':self.symbol,
            'symbol': pair,
            'volume': 0.01,
            'type': s_b,
            # 'type':  mt5.ORDER_TYPE_SELL,
            'price': order_price,
            # 'price' : mt5.symbol_info_tick(self.symbol).ask,
            'sl': 0.0,
            'tp': 0.0,
            'deviation': 30,
            'magic': 23400,
            'comment': 'py scritpt order',
            'type_time': mt5.ORDER_TIME_GTC,
            'type_fillint': mt5.ORDER_FILLING_IOC
        }

        order = mt5.order_send(requst)

        if order is None:
            ret_code = 0
        else:
            ret_code = order.retcode

        if ret_code == 10009:
            print('-------------->  SELL ORDER OK ', pair)
            df_order = pd.DataFrame(order)
            print(df_order)
        else:
            print('-------------->  SELL ORDER FAILED  ', ret_code, "  ", pair)

        return ret_code


#   MAIN

#   ---------- params execel
xcel = getExcel('C:\\MyapS\\forex\\Excels\\parms_TRADE.xlsm')
res = xcel.read_book_pandas()
if res is None:
    sys.exit(0)

symbol = res.symbol
volume = res.volume

#   ---------- trade data
show_account = accountInfo(681011, 'xQ7c932$Pm', 'IFCMarkets-Demo')
account_data = show_account.account_info()

if account_data is not None:
    account_data_df = show_account.terminal_info_df()
    account_dict = show_account.terminal_data()
    balance = account_dict['balance']

#   ---------- chek orderS  

dbpath = "C:\\Users\\User\\PycharmProjects\\vsProject\\anconda\\TRADE_4.db"
cliteACCESS = sqlUdate(dbpath)
if cliteACCESS.connect() is None:
    sys.exit(0)

order = sendOrder(681011, 'xQ7c932$Pm', 'IFCMarkets-Demo', symbol)
n = 1
#   --------- send    
while n > 0:
    rows = cliteACCESS.read_sequntial()
    df_rows = pd.DataFrame(rows, columns=['pair', 'toggle'])
    print(df_rows)
    for ind in df_rows.index:
        pair = df_rows['pair'][ind]
        toggle = df_rows['toggle'][ind]

        if toggle != 10 and toggle != 11:
            continue

        if toggle == 10:
            ercode = order.send_order(pair, 0)  # buy

        else:  # toggle = 11 :
            ercode = order.send_order(pair, 1)  # sell
        if ercode == 10009:  # OK
            cliteACCESS.change_toggle(symbol, toggle)  # reset

    print('---------------------------------------------------------------------------------- ')
    time.sleep(60)

input('')
