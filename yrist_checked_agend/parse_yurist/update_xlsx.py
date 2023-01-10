import pandas as pd

def uppend_xlsx(org, inn, date, sheet):
    df = pd.DataFrame(list(zip(org,inn,date)))
    with pd.ExcelWriter('/home/specit/data/check.xlsx', engine="openpyxl", mode="a", if_sheet_exists='overlay') as writer:
        startrow = writer.sheets[sheet].max_row
        df.to_excel(excel_writer=writer, sheet_name=sheet, startrow=startrow, header=False)
    # writer.save()

def read_xlsx():
    df = pd.ExcelFile('check.xlsx')
    for sheet in df.sheet_names:
        print(sheet)
        df_excel = pd.read_excel('check.xlsx', sheet_name=str(sheet))
        data_org = []
        data_inn = []
        data_date = []
        for row in df_excel.itertuples():
            data_org.append(row[2])
            data_inn.append(str(row[3]))
            data_date.append(row[4])
        uppend_xlsx(data_org, data_inn, data_date, str(sheet))
read_xlsx()
