import json
import logging
from asyncio import StreamWriter, StreamReader
from typing import Tuple

from core.chatter_coroutines import read_message, submit_message
from core.exceptions import InvalidTokenError

logger = logging.getLogger(__name__)


async def sign_up(conn: Tuple[StreamReader, StreamWriter], name: str) -> str:
    """
    Регистрация нового пользователя в чате и получение токена.

    :param conn: Кортеж из (StreamReader, StreamWriter) являющимися коннектом к чату девмана
    :param name: Имя пользователя
    :return: Токен
    """
    reader, writer = conn
    await read_message(reader)
    await submit_message(writer)
    await read_message(reader)
    await submit_message(writer, name)
    message = await read_message(reader)

    _, token = json.loads(message).values()
    return token


async def sign_in(conn: Tuple[StreamReader, StreamWriter], token: str):
    """
    Авторизация в чате.

    :param conn: Кортеж из (StreamReader, StreamWriter) являющимися коннектом к чату девмана
    :param token: Токен для авторизации
    """
    reader, writer = conn
    await read_message(reader)
    await submit_message(writer, token)

    data = await read_message(reader)
    if json.loads(data) is None:
        raise InvalidTokenError

    logger.debug(data)
    await read_message(reader)
