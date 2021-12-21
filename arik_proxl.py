from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from random import randint
import copy
from colors import color, red, blue
from requests.exceptions import ConnectionError
import threading
import datetime
from requests_ip_rotator import ApiGateway
import requests
import json 
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
  # Retrieve latest proxies
  user_agent_random =user_agent_rotator.get_random_user_agent()
  session = requests.Session()
  headerss=('User-Agent', user_agent_random)
  session.headers = headerss 
  proxies_req = session.get('http://www.sslproxies.org/')
  #proxies_req.add_header('User-Agent', user_agent_random)
  #proxies_doc = urlopen(proxies_req).read().decode('utf8')
  soup = BeautifulSoup(proxies_req.content, 'html.parser')
  proxies_table = soup.find('table', attrs={'class':'table table-striped table-bordered'})
  #soup = BeautifulSoup(proxies_doc, 'html.parser')
  #proxies_table = soup.find(id='proxylisttable')

  # Save proxies in the array
  proxies=[]
  for row in proxies_table.tbody.find_all('tr'):
    proxies.append({
      'ip':   row.find_all('td')[0].string,
      'port': row.find_all('td')[1].string
    })
  return proxies
def check_one(proxy) -> dict:
    """Check if proxy is working
    :proxy: dictionary {ip_port:x, anon:x, https:x, country_code:x} 
    """
    url = "http://www.otcmarkets.com/otcapi/company/profile/full/ILDO?symbol=ILDO"
    r = requests.get(
        url, proxies={'https':'https://'+proxy['ip']+':'+proxy['port']}, timeout=2)
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