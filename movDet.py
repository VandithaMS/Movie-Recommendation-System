from bs4 import BeautifulSoup
import requests

def get_movDet(name):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get('https://www.metacritic.com/movie/'+name).text

    soup = BeautifulSoup(html_content, 'html.parser')
    result = dict()

    try:
        result['title'] = soup.find("div", attrs={"class": "product_page_title"}).find('h1').text
        result['year'] = soup.find("span", attrs={"class": "release_year"}).text
        result['img'] = soup.find("img", attrs={"class": "summary_img"})['src']
        result['director'] = soup.find("div", attrs={"class": "director"}).find('a').find('span').text
        result['time'] = soup.find("div", attrs={"class": "runtime"}).find_all('span')[1].text
        result['rating'] = soup.find("div", attrs={"class": "rating"}).find_all('span')[1].text.strip()
        s = soup.find("div", attrs={"class": "summary_deck"})
        result['summary']=s.find_all('span')[2].text

        g = soup.find("div", attrs={"class": "genres"})
        l=g.find_all('span')[1]
        l=list([i for i in l if i!=','])
        result['genres'] = []
        for i in range(1,len(l),2):
            result['genres'].append(l[i].text)

        c = soup.find("div", attrs={"class": "summary_cast"})
        l=c.find_all('span')[1]
        l=list([i for i in l if i!=','])
        result['starring'] = []
        for i in range(1,len(l),2):
            result['starring'].append(l[i].text)

    except:
        pass

    return result
