import re
import csv
import urllib.request
from bs4 import BeautifulSoup, element


def get_urls():
    domain = 'https://www.verzeichnis-anwalt.de'
    url = domain + '/gerichtsverzeichnis/'
    s = BeautifulSoup(urllib.request.urlopen(url), 'html.parser')
    for link in s.select('div.courts_overview a[href]'):
        href = link['href']
        if href[0] == '/':
            yield domain + href


def get_name(s: BeautifulSoup) -> str:
    return s.select('#c_midd h2')[0].text


def get_address(s: BeautifulSoup, index: int) -> str:
    a = s.select('.detail_lawyerChambers address')[index].children
    address = [get_name(s)]
    for c in a:
        if isinstance(c, element.NavigableString) and str(c).strip():
            text = str(c).strip()
            if text != '-':
                address.append(text)
    return "\n".join(address)


def get_post_addresses(s: BeautifulSoup) -> str:
    return get_address(s, 0)


def get_house_address(s: BeautifulSoup) -> str:
    return get_address(s, 1)


def get_email(s: BeautifulSoup) -> str:
    a = s.select('.dlC_buttons a[href]')[0]
    return str(a['href']).replace('mailto:', '')


def get_web(s: BeautifulSoup) -> str:
    a = s.select('.dlC_buttons a[href]')
    if len(a) < 2:
        return ''
    return str(a[1]['href'])


def get_phone(s: BeautifulSoup) -> str:
    a = s.select('.detail_lawyerChambers')
    x = re.search(r'Tel:([^<]+)<', str(a))
    return str(x.group(1)).strip()


def get_fax(s: BeautifulSoup) -> str:
    a = s.select('.detail_lawyerChambers')
    x = re.search(r'Fax:([^<]+)<', str(a))
    return str(x.group(1)).strip()


def get_rows() -> tuple:
    fields = ['Name', 'Postanschrift', 'Hausanschrift', 'E-Mail', 'Web', 'Telefon', 'Fax']
    rows = []
    for url in get_urls():
        row = []
        print(url)
        s = BeautifulSoup(urllib.request.urlopen(url), 'html.parser')
        row.append(get_name(s))
        row.append(get_post_addresses(s))
        row.append(get_house_address(s))
        row.append(get_email(s))
        row.append(get_web(s))
        row.append(get_phone(s))
        row.append(get_fax(s))
        print(row)
        rows.append(row)
    return fields, rows


def write_excel(fields, rows, filename):
    with open(filename, 'w', newline="\n", encoding='utf8') as csv_file:
        c = csv.writer(csv_file, delimiter=';', quotechar='"')
        c.writerow(fields)
        c.writerows(rows)


def main():
    filename = 'Gerichtsadressen.csv'
    fields, rows = get_rows()
    write_excel(rows, fields, filename)


if __name__ == '__main__':
    main()
