import base64
import random
from bs4 import BeautifulSoup
import requests

def getProxyList():
    soup = BeautifulSoup(requests.get('http://free-proxy.cz/en/proxylist/country/all/https/ping/level1').content, "lxml")
    rows = soup.find('table', id="proxy_list").find('tbody').findAll('tr')
    ips = []
    for row in rows:
        tds = row.findAll('td')
        try:
            coded = tds[0].find('script').string.strip()[30:][:-3]
            ip = base64.b64decode(coded).decode('utf-8')
            port = tds[1].text
            type_ = tds[2].text
    #         if type_ != "HTTPS": continue

            ips.append({ "https": f"https://{ip}:{port}" })
        except:
            pass
    print(f"Got {len(ips)} ips")
    return ips

def getProxy(proxies):
    if not proxies:
        proxies = getProxyList()
    return proxies[random.randint(0, len(proxies)-1)]

def removeProxy(proxies, proxy_obj: object):
    proxies.remove(proxy_obj)
    print("Removed proxy", proxy_obj['https'])