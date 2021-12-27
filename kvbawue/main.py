from bs4 import BeautifulSoup

from MyFileDownloader import FileDownloader
from mail import deText

from pprint import pprint
from MyFileDownloader import FileDownloader
from bs4 import BeautifulSoup
from pathlib import Path
import csv


def gen_urls():
    fachgruppe = [(1286, 1634), (470, 155), (456, 1170), (480, 582), (481, 5410)]
    for g in fachgruppe:
        gruppe, max = g
        for offset in range(0, max + 1, 20):
            yield f"https://www.arztsuche-bw.de/index.php?suchen=1&id_fachgruppe={gruppe}&offset={offset}"


def get_file_urls(praefix='a'):
    target = 'Z:\\foo\\'
    for p in Path(target).glob(praefix + '*htm'):
        yield str(p)


def get_file_content(url):
    with open(url, "r", encoding='utf8') as file_object:
        return file_object.read()


def get_address(url: str) -> list:
    addresses = []

    data = get_file_content(url)
    s = BeautifulSoup(data, 'html.parser')
    foo = s.select('dd.name dt:first-child')
    for f in foo:
        addresses.append([f.get_text()])

    foo = s.select('dd.adresse .anschrift-arzt')
    for i, f in enumerate(foo):
        x = str(f).replace('<br>', '<br/>').split('<br/>')
        strasse = x[1]
        plz_ort = x[2].split(' ')
        plz = plz_ort[0]
        ort = ' '.join(plz_ort[1:])
        try:
            addresses[i].append(strasse)
            addresses[i].append(plz)
            addresses[i].append(ort)
        except IndexError:
            print("ERROR")
            pprint(foo)
            pprint(f)
            pprint(i)
            exit()

    # pprint(addresses)
    foo = s.select('.adresse dl dd')
    for i, f in enumerate(foo):
        x = f.select_one('a.obfuscatedEmail')
        if x is not None:
            try:
                email = deText(x.get_text())
            except IndexError:
                pprint("ERROR")
                pprint(addresses)
                pprint(x)
                pprint(x.get_text())
                pprint(deText(x.get_text()))
                exit()
        else:
            email = ''
        addresses[i].append(email)
    return addresses


def write_excel(fields, rows, filename):
    with open(filename, 'w', newline="\n", encoding='utf8') as csv_file:
        c = csv.writer(csv_file, delimiter=';', quotechar='"')
        c.writerow(fields)
        c.writerows(rows)


def main1():
    target = 'Z:\\foo\\'
    d = FileDownloader(2, target)
    prefix = "a"
    for i, url in enumerate(gen_urls()):
        # x = '"D:\\Users\\Thomas\\Documents\\Weinberger-Forum\\moodle\\Programmierung\\Justiz-Adressen\\caritas\\wget2.exe" -b -O "'+target+prefix+str(i)+'.htm" "'+ url +'"'
        x = '"C:\\Program Files\\Git\\mingw64\\bin\\curl.exe" -b -v -o "' + target + prefix + str(
            i) + '.htm" "' + url + '"'
        x = '"C:\\Program Files\\Git\\mingw64\\bin\\curl.exe" -b -v -o "' + target + prefix + str(
            i) + '.htm" "' + url + '"'
        # x = x+";\r\ntimeout /t 10;"
        # print(x)
        print(url)
        # d.get_file(url, prefix + str(i) + ".htm")


def main2():
    filename = 'kvbawue.csv'
    fields = ['Name', 'Straße', 'Plz', 'Ort', 'Email']
    #max = 5
    rows = []
    for url in get_file_urls('a'):
        #max -= 1
        #if max == 0:
        #    break
        pprint(url)
        for address in get_address(url):
            pprint(url)
            pprint(address)
            rows.append(address)
    #pprint(rows)

    write_excel(fields, rows, filename)


main2()
