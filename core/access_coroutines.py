import asyncio
import json
import logging
from asyncio import StreamWriter, StreamReader
from typing import Tuple

import aiofiles

from core.chatter_coroutines import read_message, submit_message
from core.exceptions import InvalidTokenError

logger = logging.getLogger(__name__)


async def sign_up(host: str, port: str, name: str, token_path: str):
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


async def sign_in(host: str, port: str, token: str) -> Tuple[StreamReader, StreamWriter]:
    """
    Авторизация в чате.

    :param host: IP
    :param port: Port
    :param token: Токен для авторизации
    :return:
    """
    reader, writer = await asyncio.open_connection(host, port)
    try:
        await read_message(reader)
        await submit_message(writer, token)

        data = await read_message(reader)
        if json.loads(data) is None:
            raise InvalidTokenError

        logger.debug(data)
        await read_message(reader)
    finally:
        writer.close()
        await writer.wait_closed()
    return reader, writer
