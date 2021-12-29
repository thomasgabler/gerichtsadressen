import json
import urllib
from json import JSONDecodeError
from pprint import pprint
import requests

from MyFileDownloader import FileDownloader
from bs4 import BeautifulSoup
from pathlib import Path
import csv
import html
import urllib.parse

from address.address import Address
from address.addresses import Addresses
from address.csvexporter import CsvExporter
import pickle
from address.xlsexporter import XlsExporter


# a = Addresses()
# a.add(Address('Thomas'))
# exit()


def get_file_content(url, encoding='utf-8'):
    with open(url, 'r', encoding=encoding) as f:
        return f.read()


def gen_plz():
    # url ='https://home.meinestadt.de/bayern/postleitzahlen'
    url = 'PLZ.html'
    s = BeautifulSoup(get_file_content(url), 'html.parser')
    for row in s.select('.m-table__row'):
        try:
            a = row.select('.m-textLink__linktext')
            b = row.select('td[data-label="Stadt"] div')
            plz = a[0].get_text()
            stadt = b[0].get_text().split()[0]
            yield plz, stadt
        except IndexError:
            pass


def write_excel(fields, rows, filename):
    with open(filename, 'w', newline="\n", encoding='utf8') as csv_file:
        c = csv.writer(csv_file, delimiter=';', quotechar='"')
        c.writerow(fields)
        c.writerows(rows)


def gen_data():
    files = ['ki.json', 'er.json']
    items = []
    for file in files:
        with open(file, "r", encoding='utf8') as f:
            foo = html.unescape(f.read())
            # print(foo)
            data = json.loads(foo)['data']

            for d in data:
                # key = frozenset(d.items())
                # items[key] = d
                print(d)
                name = ' '.join([d['anrede'], d['svorname'], d['sname']])
                plz = d['plz']
                ort = d['ort']
                strasse = d['strasse']
                email = d['email']
                a = Address(name=name, plz=plz, ort=ort, strasse=strasse, email=email)
                items.append(a)
                # print(key)
                # print(a)
                # exit()
            pprint(items)
            exit()
            # data = set(data)
            print(data)
            print(type(data))
            print(len(data))
            exit()


def get_file_urls(praefix='a'):
    target = 'Z:\\foo\\'
    for p in Path(target).glob(praefix + '*htm'):
        yield str(p)


def main():
    filename = 'psychokammer3.csv'
    to_delete = chr(10).join(
        [
            '{',
            ' "key": "",',
            ' "data": [',
            ' ]',
            '}'
        ])
    addresses = Addresses()
    for file in get_file_urls('b'):
        with open(file, "r", encoding='utf8') as f:
            print(file)
            try:
                foo = html.unescape(f.read()).replace(to_delete, '')
                data = json.loads(foo)['data']
                for d in data:
                    name = ' '.join([d['anrede'], d['svorname'], d['sname']]).strip()
                    plz = d['plz']
                    ort = d['ort']
                    strasse = d['strasse']
                    email = d['email']
                    a = Address(name=name, plz=plz, ort=ort, strasse=strasse, email=email)
                    addresses.add(a)
            except JSONDecodeError:
                pass
    #with open('addresses.txt', 'wb') as fh:
    #    pickle.dump(addresses, fh)
    XlsExporter.write(addresses, 'psychokammer2.xlsx')
    exit()


def gen_urls():
    # u = 'https://www.ptk-bayern.de/ptk/adressen.nsf/ptk_search_psychotherapeuten?OpenAgent&ort=&umkreis=50&name=&pgruppe=&versicherung=&wleistungen=&verfahren=&weitereverfahren=&weitereverfahren_wissen=undefined&geschlecht=&oeffentlich=&barrierefrei=&corona=undefined&sprache=&weiteresprachen=&beszg=&rnd=&data&plz='
    # u = 'https://www.ptk-bayern.de/ptk/adressen.nsf/ptk_search_psychotherapeuten?OpenAgent&umkreis=50&name=&pgruppe=&versicherung=&wleistungen=&verfahren=&weitereverfahren=&weitereverfahren_wissen=undefined&geschlecht=&oeffentlich=&barrierefrei=&corona=undefined&sprache=&weiteresprachen=&beszg=&rnd=&data&plz='
    url = 'https://www.ptk-bayern.de/ptk/adressen.nsf/ptk_search_psychotherapeuten?OpenAgent&'
    url = 'https://www.ptk-bayern.de/ptk/adressen.nsf/ptk_search_psychotherapeuten?OpenAgent&data&'

    params = {
        'umkreis': '50',
        'name': '',
        'pgruppe': '',
        'versicherung': '',
        'wleistungen': '',
        'verfahren': '',
        'weitereverfahren': '',
        'weitereverfahren_wissen': '',
        'geschlecht': '',
        'oeffentlich': '',
        'barrierefrei': '',
        'corona': '',
        'sprache': '',
        'weiteresprachen': '',
        'beszg': '',
        'rnd': '',
        # 'data': '',
    }
    for plz, ort in gen_plz():
        yield url + urllib.parse.urlencode(params | {'plz': plz, 'ort': ort})


def main0():
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'DNT': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.ptk-bayern.de/ptk/web.nsf/formular?openForm&formular=depsychotherapeutensuche',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    session = requests.Session()
    session.headers = headers
    target = "Z:\\foo\\"
    d = FileDownloader(1, target)
    prefix = "b"
    for i, url in enumerate(gen_urls()):
        print(url)
        # d.get_file(url, prefix + str(i) + ".htm")
        d.get_file(url, prefix + str(i) + ".htm", session)
        # exit()


main()

# main0()
# for data in gen_data():
#    print(data)
# for p, s in gen_plz():
#    print(p, s)
