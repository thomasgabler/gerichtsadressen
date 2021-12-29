import xlsxwriter

from address.addresses import Addresses
from pprint import pprint
import pandas as pd


class XlsExporter:
    ADDRESS_FIELDS = ['Straße', 'Plz', 'Ort']
    EMAIL_FIELD = 'E-Mail'
    NAME_FIELD = 'Name'
    JOIN_NAME = "\n"
    SHEET_NAME_ADDRESS = 'Adressen'
    SHEET_NAME_EMAIL = 'E-Mail'
    SHEET_NAME_POST = 'Post'
    SHEET_NAME_COLOR = 'Farbe'
    # Light yellow fill
    FORMAT1 = {'bg_color': '#FFEB9C', 'font_color': '#000000'}
    # Green fill
    FORMAT2 = {'bg_color': '#C6EFCE', 'font_color': '#000000'}
    FORMAT_COLUMN_PLZ = {'align': 'center','num_format': '00000'}
    FORMAT_COLUMN_NAME = {'text_wrap': True}

    @staticmethod
    def to_dataframe(addresses: Addresses) -> pd.core.frame.DataFrame:
        return pd.DataFrame.from_records([a.to_dict() for a in addresses])

    @staticmethod
    def join_field(df: pd.core.frame.DataFrame, name_field: str = 'Name') -> str:
        return XlsExporter.JOIN_NAME.join(df[name_field].tolist())

    @staticmethod
    def is_nan(item):
        if isinstance(item, str):
            return item == ''
        return isinstance(item, float)

    @staticmethod
    def combine_field(df: pd.core.frame.DataFrame, name_field: str = 'Name'):
        df2 = pd.DataFrame(df.iloc[0]).T
        df2[name_field] = XlsExporter.join_field(df, name_field)
        return df2

    @staticmethod
    def group(df: pd.core.frame.DataFrame):
        df_email = pd.DataFrame()  # with E-Mail
        df_post = pd.DataFrame()  # without E-Mail
        for address, group_address in df.groupby(XlsExporter.ADDRESS_FIELDS, dropna=False):
            has_email = False
            for email, group_email in group_address.groupby(XlsExporter.EMAIL_FIELD, dropna=False):
                combined = XlsExporter.combine_field(group_email, XlsExporter.NAME_FIELD)
                if XlsExporter.is_nan(email):
                    if not has_email:  # append to post only if item with email is not appended
                        df_post = df_post.append(combined)
                else:
                    df_email = df_email.append(combined)
                    has_email = True
        try:
            del df_post[XlsExporter.EMAIL_FIELD]
        except KeyError:
            pass
        return df_email, df_post

    @staticmethod
    def write(addresses: Addresses, filename: str = 'foo.xlsx'):
        XlsExporter.write_df(XlsExporter.to_dataframe(addresses), filename)

    @staticmethod
    def write_df(df: pd.core.frame.DataFrame, filename: str = 'foo.xlsx'):
        df.drop_duplicates(inplace=True)
        df.fillna('', inplace=True)
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        df_email, df_post = XlsExporter.group(df)

        df, df_email, df_post = XlsExporter._sort(df, df_email, df_post)

        df_sheets = [(df, XlsExporter.SHEET_NAME_ADDRESS),
                     (df_email, XlsExporter.SHEET_NAME_EMAIL),
                     (df_post, XlsExporter.SHEET_NAME_POST)]

        for d, sheet in df_sheets:
            d.to_excel(writer, sheet_name=sheet, index=False)

        sheet_address = writer.sheets[XlsExporter.SHEET_NAME_ADDRESS]
        sheet_email = writer.sheets[XlsExporter.SHEET_NAME_EMAIL]
        sheet_post = writer.sheets[XlsExporter.SHEET_NAME_POST]

        workbook = writer.book
        format_column_name = workbook.add_format(XlsExporter.FORMAT_COLUMN_NAME)  # necessary due to "\n"

        XlsExporter._write_names(df_email, sheet_email, format_column_name)
        XlsExporter._write_names(df_post, sheet_post, format_column_name)

        XlsExporter._set_columns_width(workbook, df, sheet_address, sheet_email, sheet_post)

        XlsExporter._add_color_sheet(writer, df)
        writer.save()
        print("Finished")

    @staticmethod
    def _set_columns_width(workbook: xlsxwriter.workbook.Workbook, df: pd.core.frame.DataFrame,
                           sheet_address: xlsxwriter.worksheet.Worksheet,
                           sheet_email: xlsxwriter.worksheet.Worksheet, sheet_post: xlsxwriter.worksheet.Worksheet):

        format_column_plz = workbook.add_format(XlsExporter.FORMAT_COLUMN_PLZ)

        max_length = []
        for item in list(df):
            if item == 'Plz':
                max_length.append(5)
            else:
                max_length.append(df[item].str.len().max())

        for sheet in [sheet_address, sheet_email, sheet_post]:
            for col in range(5):
                if col == 2:  # Plz should be centered
                    format = format_column_plz
                else:
                    format = None
                sheet.set_column(col, col, max_length[col] + 2, format)

    @staticmethod
    def _sort(df: pd.core.frame.DataFrame, df_email: pd.core.frame.DataFrame, df_post: pd.core.frame.DataFrame):
        sortby = ['Plz', 'Straße', 'Name', 'E-Mail']
        sortby2 = ['Plz', 'Straße', 'Name']
        try:
            df = df.sort_values(by=sortby)
            df_email = df_email.sort_values(by=sortby)
            df_post = df_post.sort_values(by=sortby2)
        except KeyError:
            pass
        return df, df_email, df_post

    @staticmethod
    def _add_color_sheet(writer, df: pd.core.frame.DataFrame):

        sheet = writer.book.add_worksheet(XlsExporter.SHEET_NAME_COLOR)
        sheet.hide()
        for r, row in enumerate(df.iterrows()):
            sheet.write(r, 0, f'=and(Adressen!B{r + 1}=Adressen!B{r + 2},Adressen!C{r + 1}=Adressen!C{r + 2})')
            sheet.write(r, 1, f'=A{r + 2}')
            if r > 0:
                a = f'A{r}'
                b = f'B{r}'
                z = f'C{r}'
                value = f'=if({z}=0,if({b},1,0),if({z}=1,if({a},1,if({b},2,0)),if({z}=2,if({a},2,if({b},1,0)),)))'
                sheet.write(r, 2, value)
        XlsExporter._conditional_format(writer, df)

    @staticmethod
    def _conditional_format(writer, df: pd.core.frame.DataFrame):

        sheet = writer.sheets[XlsExporter.SHEET_NAME_ADDRESS]
        len = df.count()[0]

        format1 = writer.book.add_format(XlsExporter.FORMAT1)
        format2 = writer.book.add_format(XlsExporter.FORMAT2)

        color_format = [(1, format1), (2, format2)]
        for color, format in color_format:
            sheet.conditional_format(f'A2:E{len}', {'type': 'formula',
                                                    'criteria': f'={XlsExporter.SHEET_NAME_COLOR}!$C2={color}',
                                                    'format': format})

    @staticmethod
    def _write_names(df: pd.core.frame.DataFrame, worksheet: xlsxwriter.worksheet.Worksheet,
                     format: xlsxwriter.format.Format, col_number: int = 0):

        for row_number, row in enumerate(df.iterrows()):
            worksheet.write(row_number + 1, col_number, row[1][XlsExporter.NAME_FIELD], format)
