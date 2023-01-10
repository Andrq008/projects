import pandas as pd

def rm_xlsx(file, search, sheet):
    if sheet == False:
        sheet = 'nalog'
    df = pd.read_excel(file, sheet_name=sheet)
    df = df.replace(r'\s+', '', regex=True)
    if int(search) not in df.values:
        return False
    return True

# if rm_xlsx('2022-09-07.xlsx', '2308147049', False):
    # print('super')