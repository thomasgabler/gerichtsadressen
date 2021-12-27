from MyFileDownloader import FileDownloader
from bs4 import BeautifulSoup
from pathlib import Path

domain = 'https://anwaltauskunft.de/'
OUT = 'Downloads'


# print(list(Path(OUT).glob('p*htm')))
# exit

def get_file_urls(praefix):
    for p in Path(OUT).glob(praefix + '*htm'):
        yield str(p)


def get_urls():
    for page in range(5958):
        url = domain + 'anwaltssuche?page=' + str(page + 1)
        yield url


def get_file_content(url):
    with open(url, 'r') as f:
        return f.read()


def get_link(url):
    s = BeautifulSoup(get_file_content(url), 'html.parser')
    for link in s.select('.lawyer-list a'):
        yield domain + link['href']


def main2():
    d = FileDownloader(30)
    for i, url in enumerate(get_file_urls('p')):
        links = get_link(url)
        for j, link in enumerate(links):
            filename = 'a' + str(i + 1) + '_' + str(j) + '.htm'
            d.get_file(link, filename)


def main():
    d = FileDownloader(50)
    for i, url in enumerate(get_urls()):
        filename = 'p' + str(i + 1) + '.htm'
        d.get_file(url, filename)


main2()
