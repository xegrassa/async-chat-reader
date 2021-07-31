import asyncio
import logging

from dotenv import load_dotenv

from core.access_coroutines import sign_up, sign_in
from core.chatter_coroutines import submit_message
from core.cli import parse_args_write
from core.exceptions import InvalidTokenError
from core.connect_coroutines import open_connection
import aiofiles


TOKEN_PATH = 'token.txt'
logger = logging.getLogger(__name__)


async def write_to_chat(arguments):
    host, port = arguments.host, arguments.port
    token, name = arguments.token, arguments.name
    async with open_connection(host, port) as conn:
        _, writer = conn

        if not token:
            logger.info('Токен не найден. Регистрация нового пользователя')
            token = await sign_up(conn, name)

            async with aiofiles.open(TOKEN_PATH, 'w', encoding='utf-8') as f:
                await f.write(f'token = {token}')

            logger.info(f'Регистрация под именем {name} завершена. Ваш токен {token} будет использоваться для подключения')

        try:
            await sign_in(conn, token)
        except InvalidTokenError:
            logger.error('Работа остановлена!!! Неизвестный токен, проверьте его или зарегистрируйте заново.')
            return

        message = arguments.message
        await submit_message(writer, message)


if __name__ == '__main__':
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s:%(module)s:%(message)s')
    ch.setFormatter(formatter)

    logging.getLogger('core.chatter_coroutines').setLevel(logging.DEBUG)
    logging.getLogger('core.chatter_coroutines').addHandler(ch)
    logging.getLogger('core.access_coroutines').setLevel(logging.DEBUG)
    logging.getLogger('core.access_coroutines').addHandler(ch)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    load_dotenv()
    args = parse_args_write()
    asyncio.run(write_to_chat(args))
