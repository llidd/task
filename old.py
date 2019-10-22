from pyzabbix import ZabbixAPI
import time
import datetime
import sys
import re

def collect():

    try:
        z = ZabbixAPI('http://77.234.203.252:8049/zabbix', user='llidd', password='yecgaa')
    except:
        print("ERROR: unable to connect to Zabbix")

    print('Enter start day (DD.MM.YYYY): ')
    fd, fm, fy = map(int, input().split('.'))
    print('Enter final day (DD.MM.YYYY): ')
    ld, lm, ly = map(int, input().split('.'))
    print('Obtaining data...')
    d_from = datetime.date(fy,fm,fd)
    d_till = datetime.date(ly,lm,ld)
    d_rng = d_till - d_from
    rng = int(str(d_rng).split()[0]) + 1


    items = z.item.get(monitored=True,output=["itemid"],filter={"value_type":3, "state":0})

    increment = 60*60*24
    counter = 0

    for item in items:
        time_from = time.mktime((fy,fm,fd,0,0,0,0,0,0))
        time_till = time.mktime((fy,fm,fd,23,59,0,0,0,0))
        history_len = 0
        history_sum = 0
        max_list=[]
        min_list=[]
        avg_list=[]
#
# Cycle for date changing
#
        for day in range(0,rng):
            data = z.history.get(history = 3, itemid=item["itemid"], time_from=time_from, time_till=time_till)
            graph  = [float(item['value']) for item in data]
            if(len(graph)!=0):
                history_max = max(graph)
                history_min = min(graph)
                history_len+=len(graph)
                history_sum+=sum(graph)
            else:
                print('No data on day',day+1)
            time_from += increment
            time_till += increment
            if(history_len!=0):
                max_list.append(history_max)
                min_list.append(history_min)
                avg_list.append(history_sum/history_len)
            else:
                max_list.append(0)
                min_list.append(0)
                avg_list.append(0)
        if((len(max_list)>0) and (len(min_list)>0) and (len(avg_list)>0)):
            t1 = min(min_list)
            t2 = max(max_list)
            total = t2 - t1
            avrg = sum(avg_list)/len(avg_list)

    return 1

def main():

    print(collect())

if __name__ == '__main__':
    main()

