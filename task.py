from pyzabbix import ZabbixAPI
import threading
import time
import datetime
import sys
import re

#
# Class for multithreading implementation
#
class theThread (threading.Thread):

   def __init__(self, backend, counter):
       threading.Thread.__init__(self)
       self.threadID = counter
       self.backend = backend

   def run(self):
       print("Starting " + self.backend + " thread")
       report(self.backend)
       print("Exiting " + self.backend + " thread")
#
# Function for collecting metric names from several backends with multithreading
#
def report(be):
    if(be == 'zabbix'):

        try:
            z = ZabbixAPI('http://77.234.203.252:8049/zabbix', user='zabbix', password='zabbix')
        except:
            print("ERROR: unable to connect to Zabbix")

        metric_names = z.item.get(monitored=True,output=["itemid"],filter={"value_type":3, "state":0}) # 10000+ metrics

        print(average(metric_names), flush=True) # flush attribute is needed for multithreading work properly

    elif(be == 'prometheus'): # Just an example
        print('Not ready yet', flush=True)

    else:
        print('Unknown backend', flush=True)
#
# Math function (average) + collecting metric values within certain dates
#
def average(items):

    try:
        z = ZabbixAPI('http://77.234.203.252:8049/zabbix', user='zabbix', password='zabbix')
    except:
        print("ERROR: unable to connect to Zabbix")

    z.timeout = 60000
#
# Enter desired date range (granularity = 1 min, 00:00-23:59)
#
    print('Enter start day (DD.MM.YYYY): ')
    fd, fm, fy = map(int, input().split('.'))
    print('Enter final day (DD.MM.YYYY): ')
    ld, lm, ly = map(int, input().split('.'))
    print('Obtaining data...')
    d_from = datetime.date(fy,fm,fd)
    d_till = datetime.date(ly,lm,ld)
    d_rng = d_till - d_from
    rng = int(str(d_rng).split()[0]) + 1

    increment = 60*60*24

    for item in items:
        time_from = time.mktime((fy,fm,fd,0,0,0,0,0,0))
        time_till = time.mktime((fy,fm,fd,23,59,0,0,0,0))
        history_len = 0
        history_sum = 0
        max_list=[]
        min_list=[]
        avg_list=[]

        for day in range(0,rng):
            data = z.history.get(history = 3, itemids=item["itemid"], time_from=time_from, time_till=time_till, sortfield="clock") # Zabbix API stuff
            graph  = [float(item['value']) for item in data] # Making data float
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
            print('Average for metric ' + item["itemid"] + ': ' + str(avrg))

def main():

#    threads = list()
    backends = ['zabbix','prometheus']

    for index, backend in enumerate(backends):
        x = theThread(backend, index) # Creating threads
#        threads.append(backend)
        x.start() # Starting threads

#    for thread in threads:
#        thread.join()

if __name__ == '__main__':
    main()
