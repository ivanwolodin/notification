import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib


class AsyncEmailSender:
    def __init__(
        self, host: str, port: str, user: str, password: str, tls=True
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.tls = tls

    async def send_mail(
        self,
        sender: str,
        to: list,
        subject: str,
        text: str,
        text_type='plain',
        cc: list = None,
        bcc: list = None,
    ):
        """
        Send an outgoing email with the given parameters.

        :param sender: From whom the email is being sent
        :param to: A list of recipient email addresses.
        :param subject: The subject of the email.
        :param text: The text of the email.
        :param text_type: Mime subtype of text, defaults to 'plain' (can be 'html').
        :param cc: A list of Cc email addresses.
        :param bcc: A list of Bcc email addresses.
        """

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(to)

        if cc:
            msg['Cc'] = ', '.join(cc)
        if bcc:
            msg['Bcc'] = ', '.join(bcc)

        msg.attach(MIMEText(text, text_type, 'utf-8'))

        smtp = aiosmtplib.SMTP(
            hostname=self.host,
            port=int(self.port),
            start_tls=False,
            use_tls=self.tls,
        )
        await smtp.connect()

        if self.tls:
            await smtp.starttls()

        if self.user:
            await smtp.login(self.user, self.password)

        await smtp.send_message(msg)
        await smtp.quit()


email_sender = AsyncEmailSender(
    host=os.getenv('SMTP_HOST'),
    port=os.getenv('SMTP_PORT'),
    user=os.getenv('SMTP_USER'),
    password=os.getenv('SMTP_PASSWORD'),
)
