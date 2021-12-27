from __future__ import annotations
from address.address import Address
from address.addresses import Addresses
from typing import Optional
import csv


class CsvExporter:
    ENCODING = 'utf8'
    NEWLINE = "\n"
    DELIMITER = ';'
    QUOTECHAR = '"'

    @staticmethod
    def write(filename: str, addresses: Addresses, max: Optional[int] = None):
        with open(filename, 'w', newline=CsvExporter.NEWLINE, encoding=CsvExporter.ENCODING) as csv_file:
            c = csv.writer(csv_file, delimiter=CsvExporter.DELIMITER, quotechar=CsvExporter.QUOTECHAR)
            c.writerow(Address.get_fields())
            for row in addresses.get_rows(max):
                c.writerow(row)
