from __future__ import annotations
from typing import Iterable, Optional

from address.address import Address
import pandas as pd


class Addresses:
    addresses: set[Address] = set()

    def __init__(self):
        self.addresses = set()

    def add(self, item: Address | Addresses | Iterable[Address]) -> Addresses:
        if isinstance(item, Address):
            self.addresses.add(item)
            return self
        elif isinstance(item, Iterable):
            self.addresses.update(item)
            return self
        elif isinstance(item, Addresses):
            self.addresses.update(item.addresses)
        else:
            Exception('Wrong address type')
        return self

    def to_dataframe(self) -> pd.core.frame.DataFrame:
        data = []
        for address in self.addresses:
            data.append(address.to_dict())
        return pd.DataFrame.from_records(data)

    def get_rows(self, max: Optional[int] = None):
        counter = max
        for address in self.addresses:
            yield address.get_row()
            if max is not None:
                counter -= 1
                if counter == 0:
                    return

    def __iter__(self):
        for a in self.addresses:
            yield a
