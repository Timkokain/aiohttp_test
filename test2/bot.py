import logging
import os

from dotenv import load_dotenv
from sessionmaker import SessionFactory
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv('TOKEN')
HOST = os.getenv('HOST')
CUSTOMER_URL = HOST + '/api/v1/customer/'
TOKEN_URL = HOST + '/api/v1/token/'
BOT_USERNAME = os.getenv('BOT_USERNAME', default='bot')
BOT_PASSWORD = os.getenv('BOT_PASSWORD', default='bot')
TEXT = 'Бот приветствует вас!'


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

session_factory = SessionFactory(TOKEN_URL, BOT_USERNAME, BOT_PASSWORD)


async def send_customer_data(
    update: Update,
    customer_url: str,
) -> None:
    """Отправляет данные клиента на сервер."""
    try:
        session = await session_factory.get_session()
        async with session:
            name = update.effective_chat.first_name
            last_name = update.effective_chat.last_name
            if last_name:
                name = ' '.join((name, last_name))
            user_data = {
                'telegram_id': update.effective_chat.id,
                'name': name,
                'username': update.effective_chat.username,
            }
            try:
                async with session.post(
                    customer_url,
                    data=user_data,
                ) as resp:
                    print(resp.status)  # временная заглушка
            except Exception as error:
                logger.error(
                    'Ошибка при выполнении HTTP запроса: %s', error)
    except Exception as error:
        logger.error('Ошибка создания ClientSession: %s', error)


async def start_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    """Обрабатывает команду '/start'."""
    await send_customer_data(update, CUSTOMER_URL)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=TEXT)


def main() -> None:
    """Запускает бота."""
    app = ApplicationBuilder().token(TOKEN).build()
    start_handler = CommandHandler('start', start_callback)
    app.add_handler(start_handler)
    app.run_polling()


if __name__ == '__main__':
    main()
