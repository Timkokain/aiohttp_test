import logging
import os

from aiohttp import ClientSession
from dotenv import load_dotenv

load_dotenv()

HOST = 'http://127.0.0.1:8000'
CUSTOMER_URL = HOST + '/api/v1/customer/'
TOKEN_URL = HOST + '/api/v1/token/'
BOT_USERNAME = os.getenv('BOT_USERNAME')
BOT_PASSWORD = os.getenv('BOT_PASSWORD')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SessionFactory:
    def __init__(self, token_url: str, username: str, password: str):
        self.token_url = token_url
        self.username = username
        self.password = password
        self.header = None

    async def get_token_header(self):
        """Obtains token, makes header template."""
        if self.header is None:
            try:
                async with ClientSession() as start_session:
                    try:
                        async with start_session.post(
                                self.token_url,
                                json={'username': self.username, 'password': self.password},
                                headers={'Content-Type': 'application/json'}
                        ) as response:
                            try:
                                response_data = await response.json()
                                token = response_data.get('access', '')
                                self.header = {'Authorization': f'Bearer {token}'}
                            except ValueError as error:
                                logger.error(
                                    "Ошибка при декодировании JSON: %s", error)
                    except Exception as error:
                        logger.error(
                            "Ошибка при выполнении HTTP запроса: %s", error)
            except Exception as error:
                logger.error("Ошибка создания ClientSession: %s", error)

    async def get_session(self) -> ClientSession:
        if self.header is None:
            await self.get_token_header()
        return ClientSession(headers=self.header)


session_factory = SessionFactory(TOKEN_URL, BOT_USERNAME, BOT_PASSWORD)
