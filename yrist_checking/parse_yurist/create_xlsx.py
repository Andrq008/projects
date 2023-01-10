import pandas as pd
from openpyxl import load_workbook
from pathlib import Path
from datetime import datetime
def xlsx (file, sheet):
    DATE = datetime.now().strftime("%Y-%m-%d")
    rem = Path(file)
    
    r = []
    b = []
    g = []
    with open(file, 'r') as t:
        columns=['Организация','ИНН','Дата']
        l = []
        for i in t.readlines():
            l.append(i.replace('\n', ''))
            if len(l)%3 == 0:
                # print('Дата: ', i.replace('\n', ''))
                g.append(i.replace('\n', ''))
            elif i.replace('\n', '').strip().isdigit():
                # print('ИНН: ', i.replace('\n', ''))
                r.append(i.replace('\n', ''))
            else:
                # print('Организация: ', i.replace('\n', ''))
                b.append(i.replace('\n', ''))
    df = pd.DataFrame(list(zip(b,r,g)), columns=columns)
    print(df)
    if Path('check.xlsx').is_file():
        with pd.ExcelWriter('check.xlsx', engine="openpyxl", mode="a") as writer:  
            df.to_excel(writer, sheet_name=sheet)
        rem.rename(f'{DATE}_{file}')
        exit(1)
    with pd.ExcelWriter('check.xlsx') as writer:
        df.to_excel(writer, sheet_name=sheet)
    # rem.unlink()
    rem.rename(f'{DATE}_{file}')
#xlsx('fssp.txt', 'test')
