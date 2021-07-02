import asyncio
import json
import logging

import aiofiles
from dotenv import load_dotenv

from cli import parse_args_write
from core.logging import configure_logging

TOKEN_PATH = 'token.txt'
configure_logging(__name__)


async def write2chat(arguments):
    logger = logging.getLogger(__name__)
    host, port = arguments.host, arguments.port
    token, name = arguments.token, arguments.name
    if not token:
        logger.info('Токен не найден. Попытка зарегистрировать нового пользователя')
        token = await register_chat(host, port, name)

    reader, writer = await asyncio.open_connection(host, port)
    try:
        await read_message(reader)
        await submit_message(writer, token)

        data = await read_message(reader)
        if json.loads(data) is None:
            print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
            return
        await read_message(reader)

        message = arguments.message
        await submit_message(writer, message)
    finally:
        writer.close()
        await writer.wait_closed()


async def register_chat(host, port, name):
    reader, writer = await asyncio.open_connection(host, port)

    await read_message(reader)
    await submit_message(writer)
    await read_message(reader)
    await submit_message(writer, name)
    message = await read_message(reader)
    _, token = json.loads(message).values()

    async with aiofiles.open(TOKEN_PATH, 'w', encoding='utf-8') as f:
        await f.write(f'token = {token}')
    return token


async def read_message(reader):
    logger = logging.getLogger(__name__)
    data = await reader.readline()
    logger.debug(data.decode())
    return data


async def authorise(host, port, token):
    logger = logging.getLogger(__name__)
    reader, writer = await asyncio.open_connection(host, port)

    await read_message(reader)
    await submit_message(writer, token)

    data = await read_message(reader)
    if json.loads(data) is None:
        print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
        return
    logger.debug(data.decode())
    await read_message(reader)


async def submit_message(writer, message: str = ''):
    logger = logging.getLogger(__name__)
    send_message = message.replace('\n', '')
    logger.debug(send_message)
    writer.write((send_message + '\n\n').encode())
    await writer.drain()


if __name__ == '__main__':
    load_dotenv()
    args = parse_args_write()
    asyncio.run(write2chat(args))
