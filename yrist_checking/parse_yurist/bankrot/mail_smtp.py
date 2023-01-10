from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# message = "Thank you"

def smtp(message):
    msg = MIMEMultipart()
    password = 'HRCfza0m475Rgm10axC7'
    msg['From'] = "seligenenko.a@maverik.ru"
    msg['To'] = "107@maverik.ru"
    msg['Subject'] = "Проверка Агентов"

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.mail.ru')                       # Создаем сессию для подключения к почтовому ящику
    server.starttls()                                           # сообщение должно быть зашифровано
    server.login(msg['From'], password)                         # Подключаемся к почтовому ящику по SMTP с использованием учетной
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


# smtp(message)