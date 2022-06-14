import webbrowser
import bs4
import lxml
import time
import json
import requests
from win10toast_click import ToastNotifier

PATH = "https://timesofindia.indiatimes.com/"
toaster = ToastNotifier()

def sections():
    req = requests.get(PATH).text
    soup = bs4.BeautifulSoup(req, 'lxml')
    nav = soup.find('nav')
    meta = nav.find_all('meta')

    web = {}
    for i in range(0, len(meta), 2):
        web[meta[i]['content']] = meta[i+1]['content']

    return web

def stories(url):
    req = requests.get(url).text
    soup = bs4.BeautifulSoup(req, 'lxml')
    script = soup.find_all('script')

    for i in range(2, len(script)):
        try:
            if script[i]['type'] == 'application/ld+json':
                dsto = script[i].text
                dsto = json.loads(dsto)
        except: continue

    news = {}
    for i in range(5):
        ds = dsto['itemListElement']
        news[ds[i]['name']] = ds[i]['url']

    return news

def link(url):
    try:
        webbrowser.open_new(url)
    except:
        pass

def notif(news):
    toaster.show_toast(
        news[0], "Click to read more",
        duration = 5,
        threaded = True,
        callback_on_click = lambda: link(news[1])
    )

def main():
    pass

if __name__ == '__main__':
    main()