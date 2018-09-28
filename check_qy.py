#!/usr/bin/env python
# -*- coding: utf-8 -*

import re
import time

log = '/usr/local/openresty/nginx/logs/access.log'
domains = []
domain_data = {}
domain_status = {}

def load_file(log_file, domains):

    with open(log_file, 'r') as log:
        for line in log.readlines():
            nodes = line.split('\t')
            if len(nodes) < 37: continue
            nodes_url = nodes[8]
            m = re.search("https?://(.+?)/", nodes_url)
            if m is None: continue
            nodes_domain = m.group(1)
            if nodes_domain not in domains : continue
            domain_data.setdefault(nodes_domain, {'clicks':0,  'status': {}})
            domain_data[nodes_domain]['status'].setdefault(nodes[4], 0)

            domain_data[nodes_domain]['clicks'] +=1
            domain_data[nodes_domain]['status'][nodes[4]] +=1

    ana_data(domain_data)
            
def ana_data(domain_data):
#    print domain_data
    now_time = time.time()
    local_time = time.strftime("%H:%M:%S", time.localtime(now_time))
    print "="*80
    for domain,data in domain_data.items():
        domain_status.setdefault(domain, {'2xx':0, '3xx':0, '4xx':0, '5xx':0})
        for k, v in data['status'].items():
            if int(k) >=200 and int(k) < 300: domain_status[domain]['2xx'] +=v
            if int(k) >=300 and int(k) < 400: domain_status[domain]['3xx'] +=v
            if int(k) >=400 and int(k) < 500: domain_status[domain]['4xx'] +=v
            if int(k) >=500 and int(k) < 500: domain_status[domain]['5xx'] +=v
    
    for domain, data in domain_status.items():
        if domain_data[domain]['clicks'] !=0:
            per_2xx = round(float(data['2xx']) / domain_data[domain]['clicks'],2)
            per_3xx = round(float(data['3xx']) / domain_data[domain]['clicks'],2)
            per_4xx = round(float(data['4xx']) / domain_data[domain]['clicks'],2)
            per_5xx = round(float(data['5xx']) / domain_data[domain]['clicks'],2)
            print 'Stamp:%s   Domain:%-30s  2xx:%.2f  3xx:%.2f  4xx:%.2f  5xx:%2.f  Clicks:%d' % (local_time, domain, per_2xx, per_3xx, per_4xx, per_5xx, domain_data[domain]['clicks'])
        else:
            print 'Stamp:%s   Domain:%-30s  2xx:0  3xx:0  4xx:0  5xx:0  Clicks:%d' % (local_time, domain, domain_data[domain]['clicks'])

if __name__ == '__main__':
 
    with open('domian.txt', 'r') as f:
        for line in f.readlines():
            line=line.strip('\n')
            domains.append(line)

    load_file(log, domains)
