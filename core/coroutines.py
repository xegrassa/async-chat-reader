import asyncio
import json
import logging
from typing import Tuple
from contextlib import asynccontextmanager
from asyncio import StreamReader, StreamWriter

import aiofiles

from core.my_logging import configure_logging

configure_logging(__name__)


async def register_in_chat(host: str, port: str, name: str, token_path: str):
    """
    Регистрация нового пользователя в чате и получение токена.

    :param host: IP
    :param port: Port
    :param name: Имя пользователя
    :param token_path: Путь до файла куда сохранить токен
    :return: Токен
    """
    reader, writer = await asyncio.open_connection(host, port)
    try:
        await read_message(reader)
        await submit_message(writer)
        await read_message(reader)
        await submit_message(writer, name)
        message = await read_message(reader)
    finally:
        writer.close()
        await writer.wait_closed()

    _, token = json.loads(message).values()
    async with aiofiles.open(token_path, 'w', encoding='utf-8') as f:
        await f.write(f'token = {token}')
    return token


async def authorise(host: str, port: str, token: str):
    logger = logging.getLogger(__name__)
    reader, writer = await asyncio.open_connection(host, port)
    try:
        await read_message(reader)
        await submit_message(writer, token)

        data = await read_message(reader)
        if json.loads(data) is None:
            print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
            return
        logger.debug(data)
        await read_message(reader)
    finally:
        writer.close()
        await writer.wait_closed()


async def read_message(reader: asyncio.StreamReader) -> str:
    logger = logging.getLogger(__name__)
    response = await reader.readline()
    logger.debug(response.decode())
    return response.decode()


async def submit_message(writer: asyncio.StreamWriter, message: str = ''):
    logger = logging.getLogger(__name__)
    send_message = message.replace('\n', '')
    logger.debug(send_message)
    writer.write((send_message + '\n\n').encode())
    await writer.drain()


@asynccontextmanager
async def open_connection(host, port) -> Tuple[StreamReader, StreamWriter]:
    """
    Контекст для открытия Асинхронного соединения и последующее его закрытие.

    :param host: IP
    :param port: Port
    :return: Reader, Writer
    """
    reader, writer = await asyncio.open_connection(host, port)
    try:
        yield reader, writer
    finally:
        writer.close()
        await writer.wait_closed()
