import imaplib   # library is used for accessing emails over imap protocol
import email   # package is a library for managing email messages
from bs4 import BeautifulSoup  # library for pulling data out of HTML and XML files
import quopri   # module performs quoted-printable transport encoding and decoding
import phonenumbers  # module for checking valid phone numbers
from scraper.models import Email_Data


def scrape_habitaclia():

    username = 'email_address'
    password = 'password'

    m = imaplib.IMAP4_SSL('imap.gmail.com')   # connect to email
    m.login(username, password)  # login to email

    m.select("Inbox/leadstest")  # selecting inbox

    result, data = m.search(None, '(SINCE "10-May-2020")')  # searching inbox

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
                raw_email)  # decoding bytes to string
            # for item1 in email_message.values():
            #     print(item1)
            subject_ = email_message['Subject']
            message_id = email_message['Message-ID']
            from_ = email_message['From']

            for part in email_message.walk():
                content_type = part.get_content_type()

                if "html" in content_type:
                    mail_html_ = part.get_payload()
                    mail_body = BeautifulSoup(mail_html_,  "html.parser")

                    # body_html = mail_body.find('div', class_='gmail_quote')
                    # soup = body_html.find('div', class_='gmail_quote')

                    data_list = []

      # -----------habitaclia----------

                    for data in mail_body.stripped_strings:

                        data_list.append(data)

                    for data in data_list:
                        if "habitaclia" in data:
                            email_data = Email_Data()
                            email_data.portal = 'habitaclia'

                            for data in mail_body.find_all('a'):
                                if 'tel' in data['href']:
                                    email_data.tel = data['href'][7:]

                            for data in data_list:
                                if 'Ref' in data:
                                    email_data.reference = data.split(
                                    )[-1]
                                elif '€' in data:
                                    email_data.price = data.split()[0]

                            for index, data in enumerate(data_list):
                                if 'Ref' in data:
                                    email_data.name = data_list[index + 2]
                                elif 'Mensaje:' in data:
                                    email_data.message = data_list[index +
                                                                   1].replace('=', '').replace('\r', '').replace('\n', '')
                                if 'Mensaje:' in data and "@" in data_list[index - 1]:
                                    email_data.email = data_list[index - 1]
                            print(email_data.portal)
                            data_list.clear()

                    data_list.clear()


print("Scraping finished")
