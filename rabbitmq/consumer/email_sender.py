import os
import smtplib
from email.message import EmailMessage

LOGIN = 'volodin.v-i-v'

PASSWORD = 'yoozuybderppauve'

DOMAIN = 'yandex.ru'
EMAIL = f'{LOGIN}@{DOMAIN}'

SMTP_HOST = 'smtp.yandex.ru'
SMTP_PORT = 465
server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
server.login(LOGIN, PASSWORD)

message = EmailMessage()
message['From'] = EMAIL
message['To'] = ",".join([EMAIL])
message['Subject'] = 'Привет!'

current_path = os.path.dirname(__file__)

data = {
    'title': 'Новое письмо!',
    'text': 'Произошло что-то интересное! :)',
    'image': 'https://pictures.s3.yandex.net:443/resources/news_1682073799.jpeg'
}


def email_send():
    try:
        server.sendmail(EMAIL, [EMAIL], message.as_string())
    except smtplib.SMTPException as exc:
        reason = f'{type(exc).__name__}: {exc}'
        print(f'Не удалось отправить письмо. {reason}')
    else:
        print('Письмо отправлено!')
    finally:
        server.close()