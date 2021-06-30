import asyncio
import json
import logging
from typing import Union

from dotenv import load_dotenv

from cli import parse_args_listen
from core.logging import configure_logging
from write2minechat import write2chat

configure_logging(__name__)


async def read_message(reader):
    logger = logging.getLogger(__name__)
    data = await reader.readline()
    logger.debug(data.decode())
    return data


async def register(reader, writer, name):
    await read_message(reader)
    await submit_message(writer)
    await read_message(reader)
    await submit_message(writer, name)
    message = await read_message(reader)
    _, token = json.loads(message).values()
    return token


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
    writer.write((send_message + '\n').encode())
    await writer.drain()


async def register_chat(host, port, name):
    reader, writer = await asyncio.open_connection(host, port)
    token = await register(reader, writer, name)

    with open('token.txt', 'w', encoding='utf-8') as f:
        f.write(token)

    await write2chat(host, port, token)


if __name__ == '__main__':
    load_dotenv()
    args = parse_args_listen()

    asyncio.run(register_chat(args.host, 5050, 'Artem'))
