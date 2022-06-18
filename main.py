import bs4
import lxml
import time
import json
import requests
import webbrowser
from win10toast_click import ToastNotifier

from scrape import *

PATH = "https://timesofindia.indiatimes.com/"
toaster = ToastNotifier()
final = {}
banner = '''  
  __         .__                         __  .__  _____ 
_/  |_  ____ |__|           ____   _____/  |_|__|/ ____\\
\   __\/  _ \|  |  ______  /    \ /  _ \   __\  \   __\ 
 |  | (  <_> )  | /_____/ |   |  (  <_> )  | |  ||  |   
 |__|  \____/|__|         |___|  /\____/|__| |__||__|   
                               \/                       
'''

def sections():
    req = requests.get(PATH).text
    soup = bs4.BeautifulSoup(req, 'lxml')
    nav = soup.find('nav')
    meta = nav.find_all('meta')

    web = {}
    for i in range(0, len(meta), 2):
        web[meta[i]['content']] = meta[i+1]['content']

    return web

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

def prompt():
    with open('user.json', 'w') as f:
        heads = sections()
        hks = list(heads.keys())
        user = {"heads":{}, "gap":5}

        print(banner)
        print('Welcome to toi-notif!\n\n')
        print('Along with the headlines, you may choose upto 4 of the following official TOI headings to receive news updates about.')
        print('Just input the numbers corresponding to your choice one at a time.\n')

        for i in range(1, len(heads)+1):
            print(f'{i:>2}. {hks[i-1]}')
        print(f'{len(heads)+1:>2}. Quit')

        print('')    

        i = 0
        while i < 4:
            try:
                ch = int(input('> '))
                if ch == len(heads)+1:
                    break
                if hks[ch-1] in user['heads']:
                    print(f'\n{hks[ch-1]} has already been selected\n')
                    continue
                user['heads'][hks[ch-1]] = heads[hks[ch-1]]
                i+=1
            except:
                print('\nValue not supported\n')

        print('\nChoices recorded! You will be notified of the top 5 articles from each of these headings per day.\n\n')

        print('In intervals of how many minutes do you want your news? (max: 30)\n')

        j = 0
        while j < 1:
            try:
                intval = float(input('> '))
                if intval > 30:
                    print('\nThe interval must be less than 30 mins\n')
                elif intval <= 0:
                    print('\nValue not supported\n')
                else:
                    user['gap'] = intval
                    j+=1
            except:
                print('\nValue not supported\n')

        json.dump(user, f)
        print('\nThank you! You are now ready to receive news updates.\n')

def main():
    try:
        with open('user.json', 'r') as f:
            data = json.load(f)
            if len(data["heads"]) == 0:
                raise Exception
    except:
        prompt()
    finally:
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
