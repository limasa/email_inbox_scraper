import imaplib   # library is used for accessing emails over imap protocol
import email   # package is a library for managing email messages
from bs4 import BeautifulSoup  # library for pulling data out of HTML and XML files
import quopri   # module performs quoted-printable transport encoding and decoding
import phonenumbers  # module for checking valid phone numbers
from scraper.models import Email_Data


def main_scraper():

    username = 'email'
    password = 'password'

    m = imaplib.IMAP4_SSL('imap.gmail.com')   # connect to email
    m.login(username, password)  # login to email

    m.select("Inbox/leadstest")  # selecting inbox

    result, data = m.search(None, 'ALL')  # searching inbox

    inbox_item_list = data[0].split()  # spliting binary data
    emails_count = len(inbox_item_list)

    if emails_count == 0:
        print('No new emails are detected!')
    else:
        print(f"Found {emails_count} new emails!")
        print("Scrapeing email data")
        for item in inbox_item_list:  # fetching binary data
            result2, data = m.fetch(item, "(RFC822)")
            raw_email = data[0][1]  # getting raw email data
            decoded_email = quopri.decodestring(
                raw_email)  # decoding bytes to string
            email_message = email.message_from_bytes(
                decoded_email)  # decoding bytes to string

            subject_ = email_message['Subject']

            from_ = email_message['From']

            for part in email_message.walk():
                content_type = part.get_content_type()

                if "html" in content_type:
                    mail_html_ = part.get_payload()
                    mail_body = BeautifulSoup(mail_html_,  "html.parser")

                    # body_html = mail_body.find('div', class_='gmail_quote')
                    # soup = body_html.find('div', class_='gmail_quote')

    # -----------Fotocasa-----------

                    data_list = []  # for fotocasa and idealista

                    for data in mail_body.stripped_strings:
                        data_list.append(data)

                    if '¡Tenemos muy buenas noticias para ti!' in data_list:
                        email_data = Email_Data()
                        email_data.portal = 'Fotocasa'

                        for data in data_list:
                            if '€' in data:
                                email_data.price = data.split()[0]
                            elif "(" and ")" in data and data[0] != '"' and data[-1] != '"':
                                data = data.split()[0].replace(
                                    '(', '').replace(')', '')
                                email_data.reference = data

                        for index, data in enumerate(data_list):
                            if data == "Mi teléfono:":
                                email_data.tel = data_list[index + 1].replace(
                                    ' ', '').replace('-', '')
                                if email_data.tel[0] and email_data.tel[1] == '0':
                                    email_data.tel = '+' + email_data.tel[2:]
                                else:
                                    pass

                            elif data == 'E-mail:':
                                email_data.email = data_list[index + 1]
                            elif 'mensaje:' in data:
                                email_data.message = data_list[index +
                                                               1].replace('\r', '').replace('\n', '')

                        email_data.save()
                        print(email_data.tel)
                        data_list.clear()
                    data_list.clear()

    # -----------Idealista-----------

                    for data in mail_body.stripped_strings:
                        data_list.append(data)

                    for data in data_list:

                        if 'Nuevo mensaje' in data:
                            email_data = Email_Data()
                            email_data.portal = 'idealista'

                            for data in data_list:
                                if 'Ref' in data:
                                    email_data.reference = data.replace(
                                        '(', '').replace(')', '')[5:]
                                elif '€' in data:
                                    email_data.price = data.split()[0]
                                elif '@' in data:
                                    email_data.email = data

                            start_index = 0
                            finish_index = 0

                            for data in mail_body.find_all('a'):
                                if 'tel' in data['href']:
                                    email_data.tel = data['href'][4:].replace(
                                        ' ', '').replace('-', '')
                                    if email_data.tel[0] and email_data.tel[1] == '0':
                                        email_data.tel = '+' + \
                                            email_data.tel[2:]
                                    else:
                                        pass

                            for index, data in enumerate(data_list):
                                if 'Nuevo mensaje' in data:
                                    start_index = index + 1
                                elif data == email_data.email:
                                    finish_index = index
                            email_data.message = ' '.join(
                                data_list[start_index:finish_index]).replace(u'\xa0', u' ')
                            print(email_data.tel)
                            data_list.clear()

                    data_list.clear()

    # ------------Kyero---------------

                    for data in mail_body.stripped_strings:
                        data_list.append(data)

                    for data in data_list:

                        if "Kyero" in data:

                            email_data = Email_Data()
                            email_data.portal = 'Kyero'

                            for index, data in enumerate(data_list):
                                if 'Nombre:' in data:
                                    email_data.reference = data_list[index - 1]
                                    email_data.name = data_list[index + 1]
                                elif "Email:" in data:
                                    email_data.email = data_list[index + 1]
                                elif "Teléfono:" in data:
                                    email_data.tel = data_list[index + 1].replace(
                                        ' ', '').replace('-', '')
                                    if email_data.tel[0] and email_data.tel[1] == '0':
                                        email_data.tel = '+' + \
                                            email_data.tel[2:]
                                    else:
                                        pass
                                elif "Mensaje:" in data:
                                    email_data.message = data_list[index +
                                                                   1].replace('\n', ' ').replace('\r', '')

                            email_data.save()
                            data_list.clear()
                            print(email_data.tel)
                    data_list.clear()

    # ------------thinkSpain----------

                    for data in mail_body.stripped_strings:
                        data_list.append(data)

                    for data in data_list:
                        if 'thinkSPAIN.com' in data:
                            email_data = Email_Data()
                            email_data.portal = 'thinkSPAIN'

                            for data in data_list:
                                if 'Name:' in data:
                                    email_data.name = data.split(
                                        ':')[-1].strip()
                                elif 'Nombre:' in data:
                                    email_data.name = data.split(
                                        ':')[-1].strip()
                                elif 'E-mail:' in data:
                                    email_data.email = data.split(
                                        ':')[-1].strip()
                                elif 'Telephone:' in data:
                                    email_data.tel = data.split(
                                        ':')[-1].strip().replace(
                                        ' ', '').replace('-', '')
                                    if email_data.tel[0] and email_data.tel[1] == '0':
                                        email_data.tel = '+' + \
                                            email_data.tel[2:]
                                    else:
                                        pass
                                elif 'Teléfono:' in data:
                                    email_data.tel = data.split(
                                        ':')[-1].strip().replace(
                                        ' ', '').replace('-', '')
                                    if email_data.tel[0] and email_data.tel[1] == '0':
                                        email_data.tel = '+' + \
                                            email_data.tel[2:]
                                    else:
                                        pass
                                elif 'Telefon:' in data:
                                    email_data.tel = data.split(
                                        ':')[-1].strip().replace(
                                        ' ', '').replace('-', '')
                                    if email_data.tel[0] and email_data.tel[1] == '0':
                                        email_data.tel = '+' + \
                                            email_data.tel[2:]
                                    else:
                                        pass
                                elif '(Your Reference' in data:
                                    email_data.reference = data.split('Your Reference', 1)[
                                        1].split()[0].replace(")", "")
                                elif '(Su referencia' in data:
                                    email_data.reference = data.split('Su referencia', 1)[
                                        1].split()[0].replace(")", "")
                                elif '(Ihre Referenz' in data:
                                    email_data.reference = data.split('Ihre Referenz', 1)[
                                        1].split()[0].replace(")", "")
                                elif 'Your Reference:' in data:
                                    email_data.reference = data.split(
                                        ": ", 1)[-1]
                                elif 'Su Referencia:' in data:
                                    email_data.reference = data.split(
                                        ": ", 1)[-1]
                                elif 'Ihre Referenz:' in data:
                                    email_data.reference = data.split(
                                        ':')[-1].strip()
                                elif 'Property:' in data:
                                    if len(data.split()) == 1:
                                        pass
                                    else:
                                        email_data.price = data.split(
                                        )[-2].replace(",", ".")
                                elif 'Propiedad:' in data:
                                    if len(data.split()) == 1:
                                        pass
                                    else:
                                        email_data.price = data.split(
                                        )[-2].replace(",", ".")
                                elif 'Immobilie:' in data:
                                    if len(data.split()) == 1:
                                        pass
                                    else:
                                        email_data.price = data.split(
                                        )[-2].replace(",", ".")
                                elif 'Objekt:' in data:
                                    if len(data.split()) == 1:
                                        pass
                                    else:
                                        email_data.price = data.split(
                                        )[-2].replace(",", ".")

                            for index, data in enumerate(data_list):
                                if 'Objekt:' in data:
                                    if len(data.split()) > 1:
                                        pass
                                    else:
                                        email_data.price = data_list[index + 1].split(
                                        )[-2].replace(",", ".")
                                elif 'Property:' in data:
                                    if len(data.split()) > 1:
                                        pass
                                    else:
                                        email_data.price = data_list[index + 1].split(
                                        )[-2].replace(",", ".")
                                elif 'Propiedad:' in data:
                                    if len(data.split()) > 1:
                                        pass
                                    else:
                                        email_data.price = data_list[index + 1].split(
                                        )[-2].replace(",", ".")
                                elif 'Immobilie:' in data:
                                    if len(data.split()) > 1:
                                        pass
                                    else:
                                        email_data.price = data_list[index + 1].split(
                                        )[-2].replace(",", ".")

                                elif 'Message:' in data:
                                    email_data.message = data_list[index + 1]
                                elif 'Mensaje:' in data:
                                    email_data.message = data_list[index + 1]
                                elif 'Nachricht:' in data:
                                    email_data.message = data_list[index + 1]
                            email_data.save()
                            data_list.clear()
                            print(email_data.tel)

                    data_list.clear()

    # -----------Luxinmo--------------------

                    for data in mail_body.stripped_strings:
                        data_list.append(data)

                    for data in data_list:
                        if 'Contact from Luxinmo Web' in data:
                            email_data = Email_Data()
                            email_data.portal = 'Luxinmo'

                            for data in data_list:
                                try:
                                    if phonenumbers.is_possible_number(phonenumbers.parse(data, 'ES')) and phonenumbers.is_valid_number(phonenumbers.parse(data, 'ES')):
                                        email_data.tel = data.replace(
                                            ' ', '').replace('-', '')
                                        if email_data.tel[0] and email_data.tel[1] == '0':
                                            email_data.tel = '+' + \
                                                email_data.tel[2:]
                                        else:
                                            pass
                                except Exception:
                                    pass
                                if '@' in data:
                                    email_data.email = data

                            for index, data in enumerate(data_list):
                                if data == 'Contact from Luxinmo Web':
                                    if "REF." in data_list[index + 3]:
                                        email_data.reference = data_list[index +
                                                                         3].split()[-1]
                                    else:
                                        email_data.name = data_list[index + 3]
                                elif data == email_data.email:
                                    email_data.message = data_list[index +
                                                                   1].replace('\n', ' ').replace('\r', '')

                            data_list.clear()
                            print(email_data.tel)
                    data_list.clear()

    # ----------------LuxuryEstate---------------------------

                    for data in mail_body.stripped_strings:
                        data_list.append(data)

                    for data in data_list:
                        if 'LuxuryEstate' in data:
                            email_data = Email_Data()
                            email_data.portal = 'LuxuryEstate'

                            for data in mail_body.find_all('a'):
                                if 'mailto' in data['href'] and 'luxuryestate' not in data['href']:
                                    email_data.email = data['href'][7:]

                            for index, data in enumerate(data_list):
                                if data == "Referencia:":
                                    email_data.reference = data_list[index + 1]
                                elif '€' in data:
                                    email_data.price = data.split(
                                        maxsplit=1)[1].replace(u'\xa0', u' ').replace(' ', '.')
                                elif data == 'Sr / Sra':
                                    email_data.name = data_list[index + 1]
                                elif data == 'Teléfono':
                                    email_data.tel = data_list[index + 1].replace(
                                        ' ', '').replace('-', '')
                                    if email_data.tel[0] and email_data.tel[1] == '0':
                                        email_data.tel = '+' + \
                                            email_data.tel[2:]
                                    else:
                                        pass
                                elif data == 'MENSAJE':
                                    email_data.message = data_list[index +
                                                                   1].replace('\n', ' ').replace('\r', '')

                            email_data.save()
                            print(email_data.tel)
                            data_list.clear()

                    data_list.clear()


print("Scraping finished")
