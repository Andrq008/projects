# -*- encoding: utf-8 -*-
 
import imaplib

mail = imaplib.IMAP4_SSL('imap.mail.ru')                        # Создаем сессию для подключения к почтовому ящику
mail.login('seligenenko.a@maverik.ru', 'HRCfza0m475Rgm10axC7')  # Подключаемся к почтовому ящику по IMAP с использованием учетной
mail.list()                                                     # Выводим список папок в почтовом ящике
mail.select("Inbox")                                            # Выбираем для работы папку входящие (inbox)

result, data = mail.search(None, "ALL")                         # Получаем массив со списком найденных почтовых сообщений
ids = data[0]                                                   # Сохраняем в переменную ids строку с номерами писем
id_list = ids.split()                                           # Получаем массив номеров писем
latest_email_id = id_list[-1]                                   # Задаем переменную latest_email_id, значением которой будет номер последнего письма
result, data = mail.fetch(latest_email_id, "(RFC822)")          # Получаем письмо с идентификатором latest_email_id (последнее письмо).
raw_email = data[0][1]                                          # В переменную raw_email заносим необработанное письмо
raw_email_string = raw_email.decode('utf-8')                    # Переводим текст письма в кодировку UTF-8 и сохраняем в переменную raw_email_string

# print(raw_email_string)

### Чтение тела письма
import email

email_message = email.message_from_string(raw_email_string)     # Получаем заголовки и тело письма и заносим результат в переменную email_message. 
if email_message.is_multipart():                                # Проверяем, является ли письмо многокомпонентным.
    for payload in email_message.get_payload():
        body = payload.get_content_subtype()
        body = payload.get_payload(decode=True).decode()
        print(body)
else:
    body = email_message.get_payload(decode=True).decode()      # Если письмо не многокомпонентное, выводим его содержимое.
    print(body)