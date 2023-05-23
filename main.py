import asyncio

from aio import get_simple_jwt_token


async def main():
    session = await get_simple_jwt_token('bot', 'bot')
    print('Received token:', token)


asyncio.run(main())
