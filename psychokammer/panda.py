import pickle

import numpy

from address.address import Address
from address.addresses import Addresses
from pprint import pprint
import pandas as pd
from address.xlsexporter import XlsExporter


def combine_names(df):
    # pprint(df)
    # names = nameToLines(df)
    # row_1 = df.iloc[0]
    df2 = pd.DataFrame(df.iloc[0]).T
    df2['Name'] = nameToLines(df)

    # columns = ['Name', 'Plz', 'Ort', 'E-Mail']
    # df3 = pd.DataFrame(columns=columns)
    # pprint(df2)
    # df3 = df3.append(df2)
    # pprint(df3)
    # exit()

    return df2
    # print("???????????????????????")
    # pprint(df2)
    # print("???????????????????????")
    # print("###", type(row_1), row_1['Ort'])
    # for _, row in df.iterrows():
    #    print("----", row['Name'], type(row)) # row = series
    #    for index, value in row.items():
    #        print(f"Index : {index}, Value : {value}")


def nameToLines(df):
    return chr(10).join(df['Name'].tolist())


def isNan(item):
    return isinstance(item, float)


pickle_off = open(
    "D:\\Users\\Thomas\\Documents\\Weinberger-Forum\\moodle\\Programmierung\\Justiz-Adressen\\psychokammer\\addresses.txt",
    "rb")
ads = pickle.load(pickle_off)
# df = addresses2df(ads)
# pprint(ads.addresses)
# pprint(df)
# exit()

# df = pd.read_csv('psychokammer2.csv', delimiter=';', quotechar='"', encoding='utf8')
filename = 'foo2.csv'
filename = r'D:\Users\Thomas\Documents\Weinberger-Forum\moodle\Programmierung\Justiz-Adressen\lpk\Landespsychotherapeutenkammer Baden-Württemberg.csv'
df = pd.read_csv(filename, delimiter=';', quotechar='"', encoding='utf8')
#df.fillna('', inplace=True)
# pprint(df['Plz'])
#XlsExporter.write(ads, 'foo3.xlsx')
XlsExporter.write_df(df,'foo3.xlsx')
exit()

# df = addresses2df(ads)
# df = ads.to_dataframe()

grouped = df.groupby(['Straße', 'Plz', 'Ort'])
rowsMitEmail = []
rowsOhneEmail = []
dfMit = pd.DataFrame()
dfOhne = pd.DataFrame()
for adr, group in grouped:
    ee = group.groupby('E-Mail', dropna=False)
    hasEmail = False
    for email, g in ee:
        combined = combine_names(g)
        if isNan(email):
            if not hasEmail:
                dfOhne = dfOhne.append(combined)
        else:
            dfMit = dfMit.append(combined)
            hasEmail = True

print("MMMMMMMMMMMMMMMMMMMMMIIIIIIIIIIIIIIIIIIIIIITTTTTTTTTTTTTTTTTTTTTT")
pprint(dfMit)
print("OOOOOOOOOOOOOOOOOHHHHHHHHHHHHHNNNNNNNNNNNNNNNNNNNEEEEEEEEEEEEE")
del dfOhne['E-Mail']
pprint(dfOhne)

writer = pd.ExcelWriter('foo.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Adressen')
dfMit.to_excel(writer, sheet_name='E-Mail')
dfOhne.to_excel(writer, sheet_name='Post')
writer.save()
