from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from random import randint
import telegram
import copy
from colors import color, red, blue
from requests.exceptions import ConnectionError
import threading
from telegram import ParseMode
import datetime
from requests_ip_rotator import ApiGateway
from proxy import scrape_proxies,check_all
import requests
import json
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import argparse
import pandas as pd
import requests
import sys
import tabulate
bad_url=[]
software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
def main():
    proxies = []
    r = requests.get(
        'https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc&speed=fast&protocols=http%2Chttps%2Csocks4%2Csocks5')
    r = r.json()
    for item in r['data']:
        proxies.append({'ip': item['ip'], 'port': item['port'], 'protocols': item['protocols'][0]})
    return proxies
def check_one(proxy) -> dict:
    """Check if proxy is working
    :proxy: dictionary {ip_port:x, anon:x, https:x, country_code:x}
    """
    url = "http://www.google.com/"
    r = requests.get(
        url, proxies={'http':proxy['protocols']+'://'+proxy['ip']+':'+proxy['port'],'https':proxy['protocols']+'://'+proxy['ip']+':'+proxy['port']},timeout=2)
    if r.status_code == 200:
        return proxy


def check_all(proxy_list) -> list:
    """Create thread pool to check all proxies
    :proxy_list: list of proxy dictionaries generated from scrape_proxies function
    """
    futures = []
    working = []

    with ThreadPoolExecutor() as executor:
        for proxy in proxy_list:
            future = executor.submit(check_one, proxy)
            futures.append(future)

        for future in futures:
            try:
                result = future.result()
                working.append(result)
            except:
                pass

    return working