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
        self.smtp = None

    async def __aenter__(self):
        self.smtp = aiosmtplib.SMTP(
            hostname=self.host,
            port=int(self.port),
            start_tls=False,
            use_tls=self.tls,
        )
        await self.smtp.connect()

        if self.tls:
            await self.smtp.starttls()

        if self.user:
            await self.smtp.login(self.user, self.password)

        return self

    async def __aexit__(self, *args):
        await self.smtp.quit()

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

        await self.smtp.send_message(msg)


async def send_email(sender: str, to: list, subject: str, text: str):
    async with AsyncEmailSender(
        host=os.getenv('SMTP_HOST'),
        port=os.getenv('SMTP_PORT'),
        user=os.getenv('SMTP_USER'),
        password=os.getenv('SMTP_PASSWORD'),
    ) as email_sender:
        await email_sender.send_mail(
            sender=sender, to=to, subject=subject, text=text
        )
