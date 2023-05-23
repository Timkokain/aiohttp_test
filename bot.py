import asyncio
import os

from aiohttp import ClientSession
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv('TOKEN')
HOST = 'http://127.0.0.1:8000'
CUSTOMER_URL = HOST + '/api/v1/customer/'
TOKEN_URL = HOST + '/api/v1/token/'
BOT_USERNAME = os.getenv('BOT_USERNAME')
BOT_PASSWORD = os.getenv('BOT_PASSWORD')
TEXT = 'Бот приветствует вас!'


async def get_simple_jwt_token(
        username: str, password: str) -> ClientSession:
    token_url = 'http://127.0.0.1:8000/api/v1/token/'

    async with ClientSession() as session:
        async with session.post(
            token_url,
            json={'username': username, 'password': password},
            headers={'Content-Type': 'application/json'}
        ) as response:
            response_data = await response.json()
            token = response_data.get('access', '')
            session.headers.update({'Authorization': f'Bearer {token}'})
            return session


async def get_session():
    return await get_simple_jwt_token('bot', 'bot')


async def start_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Handles '/start' command."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=TEXT)


def main() -> None:
    """Run bot."""
    loop = asyncio.get_event_loop()
    session = loop.run_until_complete(get_session())
    print(session.headers)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_callback))
    app.run_polling()


if __name__ == '__main__':
    main()
