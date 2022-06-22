import os
import sys
import bs4
import lxml
import time
import json
import requests
import webbrowser
import subprocess
from win10toast_click import ToastNotifier

from scrape.scrape import *

PATH = "https://timesofindia.indiatimes.com/"
toaster = ToastNotifier()
final = {}

def stories(name, url):
    req = requests.get(url).text
    soup = bs4.BeautifulSoup(req, 'lxml')
    var = '_'.join(name.replace('&', '').lower().strip().split())
    return eval(var + '(soup)')

def link(url):
    try:
        webbrowser.open_new(url)
    except:
        pass

def notif(title, url):
    if getattr(sys, 'frozen', False):
        application_path = sys.executable
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    ipath = os.path.abspath(os.path.join(os.path.dirname(application_path), 'assets/icon.ico'))
    toaster.show_toast(
        title, "Click to read more",
        duration = 5,
        threaded = True,
        icon_path = ipath,
        callback_on_click = lambda: link(url)
    )

def prompt():
    if getattr(sys, 'frozen', False):
        application_path = sys.executable
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    fpath = os.path.abspath(os.path.join(os.path.dirname(application_path), 'scrape/config.exe'))
    jpath = os.path.abspath(os.path.join(os.path.dirname(application_path), 'scrape/user.json'))
    subprocess.run([fpath, jpath])

def main():
    try:
        if getattr(sys, 'frozen', False):
            application_path = sys.executable
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))

        fpath = os.path.abspath(os.path.join(os.path.dirname(application_path), 'scrape/user.json'))
        with open(fpath, 'r') as f:
            data = json.load(f)
            if len(data) < 2:
                raise Exception
    except:
        prompt()
    else:
        fpath = os.path.abspath(os.path.join(os.path.dirname(application_path), 'scrape/user.json'))
        with open(fpath, 'r') as f:
            data = json.load(f)
            final.update(stories('headlines', PATH))

            for i in data['heads'].keys():
                final.update(stories(i, data['heads'][i]))

        for i in final:
            notif(i, final[i])
            time.sleep(data['gap']*60)

if __name__ == '__main__':
    try:
        main()
    except:
        print('Something went wrong')
        input('Press enter to exit')
