import asyncio
import json
import logging

from dotenv import load_dotenv

from core.cli import parse_args_write
from core.coroutines import register_chat, read_message, submit_message
from core.my_logging import configure_logging

TOKEN_PATH = 'token.txt'
configure_logging(__name__)


async def write2chat(arguments):
    logger = logging.getLogger(__name__)
    host, port = arguments.host, arguments.port
    token, name = arguments.token, arguments.name
    if not token:
        logger.info('Токен не найден. Попытка зарегистрировать нового пользователя')
        token = await register_chat(host, port, name, TOKEN_PATH)

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


if __name__ == '__main__':
    load_dotenv()
    args = parse_args_write()
    asyncio.run(write2chat(args))
