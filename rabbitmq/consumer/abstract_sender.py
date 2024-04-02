from abc import ABC, abstractmethod


class AsyncMessenger(ABC):
    def __init__(
        self, host: str, port: str, user: str, password: str, tls=True
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.tls = tls
        self.smtp = None

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
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
        pass
