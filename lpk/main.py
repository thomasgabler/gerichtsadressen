import length as length
from pprint import pprint
from MyFileDownloader import FileDownloader
from bs4 import BeautifulSoup
from pathlib import Path
import csv


def gen_urls():
    url = 'https://www.lpk-bw.de/archiv/psd_praxisinfo.php?id='
    for i in range(15000):
        yield url + str(i)


def get_file_urls(praefix='a'):
    target = 'Z:\\foo\\'
    for p in Path(target).glob(praefix + '*htm'):
        yield str(p)


def get_file_content(url):
    with open(url, "r", encoding='utf8') as file_object:
        return file_object.read()


def get_address(url: str) -> list:
    address = []
    data = get_file_content(url)
    s = BeautifulSoup(data, 'html.parser')
    name = ' '.join([f.get_text().strip() for f in s.select('.newsheader b')][:2]).strip()
    address.append(name)

    foo = str(s.select('tr:nth-child(3) td:first-child')).split('<br/>')
    straße_plz_ort = foo[4].split(chr(10))[1].strip().split(chr(183))
    straße = straße_plz_ort[0].strip(chr(160))
    address.append(straße)
    try:
        foo2 = straße_plz_ort[1].strip(chr(160)).strip().split(' ')
        plz = foo2[0]
        ort = foo2[1]
    except IndexError:
        plz = ''
        ort = ''
    address.append(plz)
    address.append(ort)
    try:
        email = foo[6].strip().split('E-Mail: ')[1].split(chr(160))[0]
    except IndexError:
        email = ''
    address.append(email)
    address.append(url)

    return address


def write_excel(fields, rows, filename):
    with open(filename, 'w', newline="\n", encoding='utf8') as csv_file:
        c = csv.writer(csv_file, delimiter=';', quotechar='"')
        c.writerow(fields)
        c.writerows(rows)


def main1():
    target = 'Z:\\foo\\'
    d = FileDownloader(15, target)
    prefix = "a"
    for i, url in enumerate(gen_urls()):
        d.get_file(url, prefix + str(i) + ".htm")


def main2():
    filename = 'foolpk.csv'
    fields = ['Name', 'Straße', 'Plz', 'Ort', 'Email']
    # max = 50
    rows = []
    for url in get_file_urls('a'):
        # max -= 1
        # if max == 0:
        #    break
        pprint(url)
        address = get_address(url)
        rows.append(address)
        pprint(address)

    write_excel(fields, rows, filename)


main2()
