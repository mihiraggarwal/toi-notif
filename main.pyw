import bs4
import lxml
import time
import json
import pathlib
import requests
import webbrowser
import subprocess
from win10toast_click import ToastNotifier

from scrape import *

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
    toaster.show_toast(
        title, "Click to read more",
        duration = 5,
        threaded = True,
        callback_on_click = lambda: link(url)
    )

def explorer():
    dirname = pathlib.Path(__file__).parent.resolve()
    subprocess.Popen(f'explorer {dirname}')

def prompt():
    toaster.show_toast(
        "To configure, first open config.exe",
        "Simply double click on config.exe",
        duration = 20,
        threaded = True,
        callback_on_click = explorer()
    )

def main():
    try:
        with open('user.json', 'r') as f:
            data = json.load(f)
            if len(data["heads"]) == 0:
                raise Exception
    except:
        prompt()
    else:
        with open('user.json', 'r') as f:
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
