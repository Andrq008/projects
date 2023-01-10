from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from pathlib import Path
import shutil
from datetime import datetime

# message = "Thank you"

def smtp(message, email):
    DATE = datetime.now().strftime("%Y-%m-%d")
    msg = MIMEMultipart()
    password = 'RGxBh9gjeeyjWD3fb690*'
    recipients = email
    msg['From'] = "agent_info@maverik.ru"
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = "Результат проверки"

    msg.attach(MIMEText(message, 'plain'))                      # Задаем текст тела письма

    for i in Path('/home/specit').glob('check.xlsx'):
        with open (i, 'rb') as f:
            file = MIMEApplication(f.read(), i.name)            
        file['Content-Disposition'] = 'attachment; filename="%s"' % i.name
        msg.attach(file)                                        # Загружаем файл
        shutil.move(i.name, f'/home/specit/data/{DATE}_{i.name}')

    server = smtplib.SMTP('smtp.mail.ru')                       # Создаем сессию для подключения к почтовому ящику
    server.starttls()                                           # сообщение должно быть зашифровано
    server.login(msg['From'], password)                         # Подключаемся к почтовому ящику по SMTP с использованием учетной
    server.sendmail(msg['From'], recipients, msg.as_string())
    server.quit()


# smtp(message)
smtp('Таблица с результатом проверки.\n' + 'Файл check.xlsx во вложении.', ['132@maverik.ru', '6201@maverik.ru', '6501@maverik.ru', '115@maverik.ru'])

