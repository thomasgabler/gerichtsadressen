import length as length
from pprint import pprint
from MyFileDownloader import FileDownloader
from bs4 import BeautifulSoup
from pathlib import Path
import csv


# url = "https://dienste.kvb.de/arztsuche/app/suchergebnisse.htm?hashwert=f574b9d9d25bcb96a1c3784199b763&resultCount=1000"
# url2 = "https://dienste.kvb.de/arztsuche/app/suchergebnisse.htm?zeigeKarte=false&resultCount=1000&hashwert=f574b9d9d25bcb96a1c3784199b763&page="


def get_file_urls(praefix):
    OUT = "Downloads"
    for p in Path(OUT).glob(praefix + '*htm'):
        yield str(p)


def get_file_content(url):
    with open(url, "r", encoding='utf8') as file_object:
        return file_object.read()


def gen_urls():
    # url = "https://dienste.kvb.de/arztsuche/app/suchergebnisse.htm?zeigeKarte=false&resultCount=90000&hashwert=f574b9d9d25bcb96a1c3784199b763&page="
    url = "https://dienste.kvb.de/arztsuche/app/suchergebnisse.htm?zeigeKarte=false&resultCount=90000&hashwert=d1f399332fe2356379ecea345aa10e5&page="
    for i in range(1, 9001):
        yield url + str(i)


def parse_address(f) -> dict:
    address = {}
    text_list = []
    first = True
    for u in f.select("td"):
        utext = u.get_text().strip()
        if first:
            first = False
            vor = utext
            continue
        if utext:
            for uu in utext.split(chr(160)):
                text_list.append(uu)
    if vor:
        vor_list = vor.split(',')
    else:
        vor_list = []
    address['Vor_Straße'] = vor
    if len(text_list) == 4:
        address['Straße'] = text_list[0] + ' ' + text_list[1]
        address['Plz'] = text_list[2]
        address['Ort'] = text_list[3]
    else:
        print("len=", len(text_list))
        print(vor_list)
        exit(text_list)
    return address


def get_address(url: str) -> list:
    addresses = []
    data = get_file_content(url)
    s = BeautifulSoup(data, 'html.parser')
    for index, f in enumerate(s.select(".titel_name_zelle")):
        name = f.get_text().strip()
        addresses.append({'Name': name})

    for index, f in enumerate(s.select(".fachgebiet_zelle")):
        fachgebiete = []
        select_fachgebiete = f.get_text()
        for x in select_fachgebiete.split('\n'):
            if x.strip():
                fachgebiete.append(x.strip())
        addresses[index]['Fachgebiete'] = ','.join(fachgebiete)

    foo = s.select(".adresse_tabelle")
    for index, f in enumerate(foo):

        a = parse_address(f)
        # print(a)
        for key, value in parse_address(f).items():
            addresses[index][key] = value
        print(addresses)
        # exit()


"""
        xx = f.select("td")
        sonst_addresse = xx[0].get_text().strip()
        strasse_hsn = xx[1].get_text().strip()
        plz_orte = xx[2].get_text().split(chr(160))
        plz = plz_orte[0].strip()
        ort = plz_orte[1].strip()
        x = strasse_hsn.split(chr(160))
        strasse = ' '.join(x)
        addresses[index]['Plz'] = plz
        addresses[index]['Ort'] = ort
        addresses[index]['Straße'] = strasse
        addresses[index]['Vor_Straße'] = sonst_addresse

        if sonst_addresse and not strasse:
            parse_address(f)
            exit()
"""

    foo = s.select(".tel_tabelle")
    for index, f in enumerate(foo):
        x = f.select('a[href^="mailto:"]')
        if x:
            email = x[0].get_text()
        else:
            email = ''
        x = f.select('a[href^="http"]')
        if x:
            web = x[0].get_text()
        else:
            web = ''
        addresses[index]['Email'] = email
        addresses[index]['Web'] = web

    foo = s.select(".adresse_zelle >span")
    for index, f in enumerate(foo):
        addresses[index]['Praxis'] = f.get_text().strip()
    # print(addresses)
    # exit()
    return addresses


def get_addresses(max=999):
    prefix = "a"
    addresses = []
    for url in get_file_urls(prefix):
        max = max - 1
        if max < 0:
            break
        for address in get_address(url):
            addresses.append(address)
    return addresses


def write_excel(fields, rows, filename):
    with open(filename, 'w', newline="\n", encoding='utf8') as csv_file:
        c = csv.writer(csv_file, delimiter=';', quotechar='"')
        c.writerow(fields)
        c.writerows(rows)


def main1():
    d = FileDownloader(15)
    prefix = "a"
    for i, url in enumerate(gen_urls()):
        d.get_file(url, prefix + str(i) + ".htm")


def main():
    max = 999
    filename = 'kvb.csv'
    fields = ['Name', 'Fachgebiete', 'Vor_Straße', 'Straße', 'Plz', 'Ort', 'Email', 'Web', 'Praxis']
    addresses = get_addresses(max)
    print(addresses, len(addresses))
    rows = []

    for address in addresses:
        row = []
        for field in fields:
            row.append(address[field])
        rows.append(row)

    write_excel(fields, rows, filename)


main()
