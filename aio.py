import asyncio

import aiohttp


async def get_simple_jwt_token(
        username: str, password: str) -> aiohttp.ClientSession:
    token_url = 'http://127.0.0.1:8000/api/v1/token/'

    async with aiohttp.ClientSession() as session:
        async with session.post(
            token_url,
            json={'username': username, 'password': password},
            headers={'Content-Type': 'application/json'}
        ) as response:
            response_data = await response.json()
            token = response_data.get('access', '')
            session.headers.update({'Authorization': f'Bearer {token}'})
            return session


session = asyncio.run(get_simple_jwt_token('bot', 'bot'))
print(session.headers)
