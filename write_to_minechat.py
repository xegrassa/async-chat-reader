import asyncio
import json
import logging

from dotenv import load_dotenv

from core.cli import parse_args_write
from core.coroutines import register_in_chat, read_message, submit_message, open_connection
from core.my_logging import configure_logging

TOKEN_PATH = 'token.txt'
configure_logging(__name__)


async def write_to_chat(arguments):
    logger = logging.getLogger(__name__)
    host, port = arguments.host, arguments.port
    token, name = arguments.token, arguments.name
    if not token:
        logger.info('Токен не найден. Попытка зарегистрировать нового пользователя')
        token = await register_in_chat(host, port, name, TOKEN_PATH)

    async with open_connection(host, port) as conn:
        reader, writer = conn
        await read_message(reader)
        await submit_message(writer, token)

        data = await read_message(reader)
        if json.loads(data) is None:
            print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
            return
        await read_message(reader)

        message = arguments.message
        await submit_message(writer, message)


if __name__ == '__main__':
    load_dotenv()
    args = parse_args_write()
    asyncio.run(write_to_chat(args))
