


#region info & todo
# connect.py
# full path C:\Users\User\PycharmProjects\vsProject\anconda\mq5_py\.idea\connect.py
# this app link https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py
# link to functions https://www.mql5.com/en/docs/integration/python_metatrader5/mt5copyratesfrom_py
# tutorial folder C:\Users\User\Videos\TUtorials\python\mq5
# tutoial name:Connect Python to MetaTrader5

# C:\Users\User\PycharmProjects\vsProject\anconda\mq5_py\.vscode\launch.json

# TO DO: 
#endregion
from datetime import datetime
import time
import MetaTrader5 as mt
import pandas as pd
# from datetime  import datet
import plotly.express  as px

mt.initialize()

login=681011
password="xQ7c932$Pm"
server="IFCMarkets-Demo"
mt.login(login,password,server)

account_info=mt.account_info()
print (account_info)
login_numer=account_info.login
balance= account_info.balance
equity =account_info.equity
print ('\nlogin balance  equity {} {} {}'.format(login_numer,balance,equity))
symbols=mt.symbols_total()
# symbols_info=mt.symbol_info('EURUSD')._asdict()
symbols_info=mt.symbol_info('EURUSD')
print(symbols_info)
sym_df=pd.DataFrame(symbols_info)
print(sym_df)
symbol_price=mt.symbol_info_tick('EURUSD')._asdict()
ochl_data=pd.DataFrame(mt.copy_rates_range('EURUSD',
                                      mt.TIMEFRAME_D1,
                                      datetime(2021,1,11),
                                      datetime.now())) 
fig=px.line(ochl_data,x=ochl_data['time'],y=ochl_data['close'])
# fig.show()

# tick_data=pd.DataFrame(mt.copy_ticks_range('EURUSD',
#                        datetime(2021,10,4),
#                         datetime.now(),
#                         mt.COPY_TICKS_ALL))
# fig=px.line(tick_data,x=tick_data['time'],y=[tick_data['bid'],tick_data['ask']])
# fig.show()

num_orders=mt.orders_total()
orders=mt.orders_get()
num_positions=mt.positions_total()
positions=mt.positions_get()
num_orders_history=mt.history_orders_total(datetime(2021,1,1),datetime.now())
order_history=mt.history_orders_get(datetime(2021,1,1),datetime.now())
num_deal_history =mt.history_deals_total(datetime(2021,1,1),datetime.now())
deal_history=mt.history_deals_get(datetime(2021,1,1),datetime.now())
requst={
    'action': mt.TRADE_ACTION_DEAL,
    'symbol':'EURUSD',
    'volume' :0.01, 
    'type':  mt.ORDER_TYPE_BUY,
    'price' : mt.symbol_info_tick('EURUSD').ask,
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
print(order)
# order.retcode != mt5.TRADE_RETCODE_DONE
input  ('')



