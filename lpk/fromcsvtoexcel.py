import pandas as pd
from address.xlsexporter import XlsExporter

csv = 'Landespsychotherapeutenkammer Baden-Württemberg.csv'
df = pd.read_csv(csv, delimiter=';', quotechar='"', encoding='utf8')

XlsExporter.write_df(df, 'Landespsychotherapeutenkammer Baden-Württemberg2.xlsx')
exit()