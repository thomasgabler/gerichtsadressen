import re
import csv
import urllib.request
import gzip

from bs4 import BeautifulSoup, element
import json
from pprint import pprint
from pathlib import Path

domain = 'https://anwaltauskunft.de/'
# OUT = "D:\\Users\\Thomas\\Documents\\Weinberger-Forum\\moodle\\Programmierung\\Justiz-Adressen\\Anwälte\\daten\\foo"
OUT = "D:\\Users\\Thomas\\Documents\\Weinberger-Forum\\moodle\\Programmierung\\Justiz-Adressen\\Downloads"


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


def get_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11",
        "Referer": "https://anwaltauskunft.de/",
        "Accept-Encoding": "compress, gzip"
    }
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req).read()
    return gzip.decompress(response).decode()


def get_link(url):
    # s = BeautifulSoup(get_content(url), 'html.parser')
    s = BeautifulSoup(get_file_content(url), 'html.parser')
    for link in s.select('.lawyer-list a'):
        yield domain + link['href']


def get_text(tag):
    if tag is None:
        return ''
    return tag.text.strip()


def parse_lawyer(url):
    row = []
    # tag = BeautifulSoup(get_content(url), 'html.parser')
    tag = BeautifulSoup(get_file_content(url), 'html.parser')
    # tag = BeautifulSoup(get_file_content(url), 'html.parser')
    Beruf = get_text(tag.select_one('.job-title strong'))
    Name = get_text(tag.select_one('.name'))

    address = tag.select_one('.lawyer-address')
    if address is None:
        Straße = ''
        PLZ = ''
        Ort = ''
    else:
        Straße = get_text(address.select_one('span[itemprop=streetAddress]'))
        PLZ = get_text(address.select_one('span[itemprop=postalCode]'))
        Ort = get_text(address.select_one('span[itemprop=addressLocality]'))

    contact = tag.select_one('.lawyer-profile-contact')
    if contact is None:
        Telefon = ''
        Email = ''
    else:
        Telefon = get_text(contact.select_one('.anwa-icon-phone + a'))
        Email = get_text(contact.select_one('.anwa-icon-mail + a'))

    fachanwaelte = [f.text for f in tag.select('.lawyer-professional-advocacies .badge')]
    for i in range(5 - len(fachanwaelte)):
        fachanwaelte.append('')

    rechtsgebiete = [f.text for f in tag.select('.lawyer-sections .badge')]
    for i in range(20 - len(rechtsgebiete)):
        rechtsgebiete.append('')

    row.append(Beruf)
    row.append(Name)
    row.append(Straße)
    row.append(PLZ)
    row.append(Ort)
    row.append(Telefon)
    row.append(Email)
    row = row + fachanwaelte + rechtsgebiete
    return row


def main():
    header = ['Beruf', 'Name', 'Straße', 'PLZ', 'Ort', 'Telefon', 'E-Mail', 'Fachanwalt für 1', 'Fachanwalt für 2',
              'Fachanwalt für 3', 'Fachanwalt für 4', 'Fachanwalt für 5', 'Rechtsgebiet 1', 'Rechtsgebiet 2',
              'Rechtsgebiet 3', 'Rechtsgebiet 4', 'Rechtsgebiet 5', 'Rechtsgebiet 6', 'Rechtsgebiet 7',
              'Rechtsgebiet 8', 'Rechtsgebiet 9', 'Rechtsgebiet 10', 'Rechtsgebiet 11', 'Rechtsgebiet 12',
              'Rechtsgebiet 13', 'Rechtsgebiet 14', 'Rechtsgebiet 15', 'Rechtsgebiet 16', 'Rechtsgebiet 17',
              'Rechtsgebiet 18', 'Rechtsgebiet 19', 'Rechtsgebiet 20']
    with open('foo.csv', 'w', encoding='utf-8') as f:
        maxRows = 0
        writer = csv.writer(f, delimiter=';', lineterminator='\n')
        writer.writerow(header)
        for link in get_file_urls('a'):
            maxRows = maxRows + 1
            print(maxRows)
            # if maxRows <= 0:
            #    exit(0)
            row = parse_lawyer(link)
            writer.writerow(row)


main()
