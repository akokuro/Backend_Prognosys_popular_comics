from bs4 import BeautifulSoup
import requests
import pprint
import re


def pars_readmanga(url: str):
    page = 1
    offset = 70
    titles = []
    while True:
        try:
            url = url + '&offset=' + str(offset * page) if page > 1 else url
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "lxml")
            titles_links = soup.body("div", {"class": "tile"})
            links = []
            for link in titles_links:
                links.append('https://readmanga.live' + link.h3.a['href'])
            for link in links:
                print(link)
                titles.append(pars_title(link))

            page += 1
            if page == 2:
                break
        except Exception as ex:
            print('Error:', ex)

    pprint.pprint(titles)


def pars_mangalib(url: str):
    page = 1
    titles = []
    while True:
        try:
            url = url + str(page)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "lxml")
            titles_links = soup.body("div", {"class": "media-card-wrap"})
            links = []
            for link in titles_links:
                links.append(link.a['href'])
                print(link.a['href'])

            for link in links:
                print(link)
                titles.append(pars_title(link, False, True))
            page += 1
            if page == 2:
                break
        except Exception as ex:
            print('Error:', ex)
    pprint.pprint(titles)


def pars_title(link, readmanga=True, mangalib=False):
    f = open('title.txt','rb') 
    content = f.read() 
    soup = BeautifulSoup(content, "lxml")
    if readmanga:   
        title_name = soup.find("meta", itemprop="name")['content'] \
            if soup.find("meta", itemprop="name") else None
        genres = {el.a.text for el in soup.body(
            "span", {"class": "elem_genre"})}
        category = soup.body.find("span", {"class": "elem_category"}).a.text \
            if soup.body.find("span", {"class": "elem_category"}) else None
        year = soup.body.find("span", {"class": "elem_year"}).a.text \
            if soup.body.find("span", {"class": "elem_year"}) else None
        for div in soup.body.findAll("div", {"class": "rightBlock"}):
            if div.h5:
                if div.h5.text == 'Количество закладок':
                    for i, strong in enumerate(div.findAll('strong')):
                        if i == 0:
                            status_process = strong.text
                        if i == 1:
                            status_readed = strong.text
                        if i == 2:
                            status_loved = strong.text
        return {'title_name': title_name, 'genres': genres, 'category': category, 'year': year, 
            'status_process': status_process, 'status_readed': status_readed, 'status_loved': status_loved}
    elif mangalib:
        title_name = soup.find("meta", itemprop="name")['content'] \
            if soup.find("meta", itemprop="name") else None
        for info in soup.body("div", {"class": "info-list__row"}):
            info_name = info.strong.text
            info_value = info.span.text if info.span else None
            if info_name == "Тип":
                category = info_value
            elif info_name == "Дата релиза":
                year = info_value
            elif info_name == "Жанры":
                genres = {el.text for el in info.findAll("a")}
            elif info_name == "Просмотров":
                views_count = info_value
        bookmarks_count_text = soup.body.find("h3", {"class": "aside__title"})
        bookmarks_count = re.match(r"\(.*?\)", bookmarks_count_text)[1:-1]
        return {'title_name': title_name, 'genres': genres, 'category': category, 'year': year, 'views_count': views_count}

    
def save_title_file(link):
    response = requests.get(link)
    f = open('title.txt','wb') 
    print(response.content)
    f.write(response.content)


if __name__ == '__main__':
    # pars_readmanga('https://readmanga.live/list?sortType=created')
    # pars_mangalib('https://mangalib.me/manga-list?sort=created_at&dir=desc&page=')
    save_title_file('https://mangalib.me/ilwojil-su-eobsneun-manyeoui-somang')
    pprint.pprint(pars_title(
        'https://mangalib.me/ilwojil-su-eobsneun-manyeoui-somang', False, True))
