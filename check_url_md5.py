
import requests
import hashlib
from datetime import datetime
import argparse


My_UA = "Dnion-UA-ck-md5"

def get_data(url,ip,ua):
    proxy = {
        'http': 'http://' + ip
    }
    head = {
        'user-agent': ua,
        'Range': 'bytes= 0-1000'
    }
    req = requests.get(url, headers=head, timeout=5, proxies=proxy)
    return req


def action(url, ip, ua):
    try:
        resault = get_data(url, ip, ua)
        md = md5_sum(resault.content)
        url_len = len(url)
        if url_len >= 60:
            url_out = url[0:25] + "..." + url[-25:]
        else:
            url_out = url
        if resault.status_code == 200 or resault.status_code == 206:
            print('\033[32m%-4s\033[0m %-15s %-35s %-1s %-15s %-1s %-10s' \
            %(resault.status_code, ip, url_out, ' ', md, '   ', resault.headers["Server"]))
        else:
            print('\033[34m%-4s %-15s %-35s %-1s %-15s %-1s %-10s\033[0m' \
            %(resault.status_code, ip, url_out, ' ', md, '   ', resault.headers["Server"]))
        
    except requests.exceptions.ConnectTimeout as ERROR_Timeout:
        print("     \033[31mFailed to connect %-15s due to connect time out\033[0m" %ip)
    except requests.exceptions.ProxyError as ERROR_Proxy_failed:
        print("     \033[31mFailed to connect %-15s due to refaused\033[0m" %ip)
    except KeyboardInterrupt as ERROR_User_Stop:
        print("\n     \033[31mYou stoped it at %-15s\033[0m" %ip)
        sys.exit(0)
    except requests.exceptions.ReadTimeout as ERROR_Read_Time_Out:
        print("     \033[31mFailed to connect %-15s due to read time out\033[0m" %ip)


def md5_sum(data):
    data_md5 = hashlib.md5()
    data_md5.update(data)
    md5sum = data_md5.hexdigest()
    return  md5sum

def _argparse():
    
    parser = argparse.ArgumentParser(description='A Python-check url md5 script!')
    parser.add_argument('-u', '--url', action='store', dest='url', required=True, help='check url')
    parser.add_argument('-f', '--file', action='store', dest='file', required=True, 
                        help='check IP')
    parser.add_argument('-s', action='store', dest='source', help='check the source IP')
    return parser.parse_args()


def main():
    parser = _argparse()
    conn_args = dict(url=parser.url, file=parser.file, source=parser.source)
    return conn_args
    print(conn_args)
    

if __name__ == '__main__':
    conn_args = main()
    if conn_args['source']:
        with open(conn_args['file']) as f:
            for line in f.readlines():
                ip = line.strip('\n')
                url = conn_args['url'] 
                action(url, ip, My_UA)
        print("\033[32m \n     Source inspection results is: \033[0m")
        action(url, conn_args['source'], My_UA)
        print("\n")
    else:
        with open(conn_args['file']) as f:
             for line in f.readlines():
                ip = line.strip('\n')
                url = conn_args['url']
                action(url, ip, My_UA)
