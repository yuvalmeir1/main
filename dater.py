#region data and info

# dater.py
# script locaion  C:\Users\User\PycharmProjects\vsProject\anconda\mq5_py\dater.py
# web epoch time sample https://www.kite.com/python/answers/how-to-convert-epoch-time-to-datetime-in-python

#endregion 


import datetime
import sys
import pdb
pdb.set_trace 

def epoch_to_date(ts_epoch):  # return list of date time 
    # ts = datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d %H:%M:%S')
    # breakpoint()
    # print("date is ",ts)
    # ts = datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y,%m,%d,%H,%M')
    ts = datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y,%m,%d,%H')

    datess=[None]


    datess.append((datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y')))
    datess.append((datetime.datetime.fromtimestamp(ts_epoch).strftime('%m')))
    datess.append((datetime.datetime.fromtimestamp(ts_epoch).strftime('%d')))
    datess.append((datetime.datetime.fromtimestamp(ts_epoch).strftime('%H')))
    datess.append((datetime.datetime.fromtimestamp(ts_epoch).strftime('%M')))
    # breakpoint()
    return datess


def epoch_to_datetime(ts_epoch):    # return string of date time

    ts = datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d %H:%M:%S')
    # c_date=int(datetime.datetime.utcnow().timestamp(mmm))
    print("date is ",ts)
    # breakpoint()
    return ts

