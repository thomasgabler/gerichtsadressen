import pandas as pd
from address.xlsexporter import XlsExporter

csv = 'kvbawue.csv'
df = pd.read_csv(csv, delimiter=';', quotechar='"', encoding='utf8')
#df.drop_duplicates(inplace=True)

XlsExporter.write_df(df, 'kvbawue2.xlsx')
exit()
