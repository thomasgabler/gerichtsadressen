from __future__ import annotations
from dataclasses import dataclass
from pprint import pprint


@dataclass
class Address:
    name: str
    strasse: str
    plz: str
    ort: str
    email: str

    def __init__(self, name='', strasse='', plz='', ort='', email=''):
        if name is None:
            name = ''
        if strasse is None:
            strasse = ''
        if plz is None:
            plz = ''
        if ort is None:
            ort = ''
        if email is None:
            email = ''

        self.name = name
        self.strasse = strasse
        self.plz = plz
        self.ort = ort
        self.email = email

    def __hash__(self) -> int:
        return (self.name + self.strasse + self.plz + self.ort + self.email).__hash__()

    def get_row(self) -> list:
        return [self.name, self.strasse, self.plz, self.ort, self.email]

    def to_dict(self) -> dict:
        return {'Name': self.name, 'Straße': self.strasse, 'Plz': self.plz, 'Ort': self.ort, 'E-Mail': self.email}

    @staticmethod
    def get_fields() -> list:
        return ['Name', 'Straße', 'Plz', 'Ort', 'E-Mail']
