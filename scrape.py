import json

PATH = "https://timesofindia.indiatimes.com"

def headlines(soup):
    anchor = soup.find_all('a')
    news = {}
    n = 0
    for i in anchor:
        if i.find('figcaption') is None:
            continue
        news[i.find('figcaption').text] = i['href']
        n += 1
        if n >= 5:
            break

    return news

def briefs(soup):
    head = soup.find_all('h2')
    news = {}
    n = 0
    for i in head:
        if i.find('a') is None:
            continue
        news[i.text] = PATH + i.find('a')['href']
        n += 1
        if n >= 5:
            break
    
    return news

def videos(soup):
    fig = soup.find_all('figure')
    news = {}
    for i in range(5):
        news[fig[i].find('a')['title']] = fig[i].find('a')['href']
    
    return news

def city(soup):
    return headlines(soup)

def india(soup):
    script = soup.find_all('script')
    for i in range(2, len(script)):
        try:
            if script[i]['type'] == 'application/ld+json':
                global dsto
                dsto = script[i].text
                dsto = json.loads(dsto)
                break
        except: 
            continue

    news = {}
    for k in range(5):
        ds = dsto['itemListElement']
        news[ds[k]['name']] = ds[k]['url']

    return news

def world(soup):
    return india(soup)

def business(soup):
    return headlines(soup)

def tech(soup):
    return headlines(soup)

def cricket(soup):
    anchor = soup.find_all('a')
    news = {}
    n = 0
    for i in anchor:
        try:
            if i['class'] != ['w_img']:
                continue
        except:
            continue
        news[i['title']] = PATH + i['href']
        n += 1
        if n >= 5:
            break
    
    return news

def sports(soup):
    return cricket(soup)

def entertainment(soup):
    anchor = soup.find_all('a')
    news = {}
    n = 0
    for i in anchor:
        try:
            if i['data-action'] != 'Navigation_NewsItem':
                continue
        except:
            continue
        news[i['data-title']] = PATH + i['href']
        n += 1
        if n >= 5:
            break
    
    return news

def games(soup):
    head = soup.find_all('h4')
    news = {}
    n = 0
    for i in head:
        try:
            if i['class'] != ['_1K1MK']:
                continue
        except:
            continue
        slug = '-'.join(i.text.lower().partition(' - ')[0].split())
        news[i.text.partition(' - ')[0]] = PATH + f'/games/{slug}'
        n += 1
        if n >= 4:
            break

    return news

def tv(soup):
    anchor = soup.find_all('a')
    news = {}
    n = 0
    for i in anchor:
        try:
            if i['data-label'] == 'Featured' and i['title']:
                news[i['title']] = PATH + i['href']
                n += 1
            if n >= 5:
                break
            else:
                continue
        except:
            continue
    
    return news

def web_series(soup):
    anchor = soup.find_all('a')
    news = {}
    n = 0
    for i in anchor:
        try:
            if i['data-action'] == 'SectionListing_NewsItem' and i['href'] != 'javascript://':
                news[i.find('img')['title']] = PATH + i['href']
                n += 1
            if n >= 5:
                break
            else:
                continue
        except:
            continue
    
    return news

def life_style(soup):
    anchor = soup.find_all('a')
    news = {}
    n = 0
    for i in anchor:
        try:
            if i['data-section'] != "2886714":
                continue
        except:
            continue
        news[i['data-title']] = PATH + i['href']
        n += 1
        if n >= 5:
            break
    
    return news

def education(soup):
    div = soup.find_all('div')
    news = {}
    for i in div:
        try:
            if i['id'] == 'c_wdt_list_1':
                anchor = i.find_all('a') 
        except:
            continue
    
    for n in range(5):
        news[anchor[n]['title']] = PATH + anchor[n]['href']
    
    return news

def photos(soup):
    anchor = soup.find_all('a')
    news = {}
    n = 0
    for i in anchor:
        try:
            if 'photohomenavsec7str' in i['pg']:
                news[i['title']] = i['href']
                n += 1
            if n >= 5:
                break
        except:
            continue
        
    return news
