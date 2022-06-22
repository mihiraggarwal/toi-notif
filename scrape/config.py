import os
import sys
import bs4
import lxml
import json
import requests

PATH = "https://timesofindia.indiatimes.com/"
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

def prompt():
    try:
        pth = sys.argv[1]
    except:
        if getattr(sys, 'frozen', False):
            application_path = sys.executable
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        pth = os.path.abspath(os.path.join(os.path.dirname(application_path), 'user.json'))

    with open(pth, 'w') as f:
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
        input('Press enter to exit')

if __name__ == '__main__':
    try:
        prompt()
    except:
        print('Something went wrong')
        input('Press enter to exit')
