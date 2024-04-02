import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
from abstract_sender import AsyncMessenger


class AsyncEmailSender(AsyncMessenger):
    async def connect(self):
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

    async def disconnect(self):
        await self.smtp.quit()

    async def send_message(
        self,
        sender: str,
        to: list,
        subject: str,
        text: str,
        text_type='plain',
        cc: list = None,
        bcc: list = None,
    ):
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
        await email_sender.send_message(
            sender=sender, to=to, subject=subject, text=text
        )
