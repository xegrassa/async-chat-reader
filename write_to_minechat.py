import asyncio
import logging

from dotenv import load_dotenv

from core.cli import parse_args_write
from core.coroutines.chatter import submit_message
from core.coroutines.connect import open_connection
from core.coroutines.files import write_token
from core.coroutines.login import sign_up, sign_in
from core.exceptions import InvalidTokenError

TOKEN_PATH = 'token.txt'
logger = logging.getLogger(__name__)


async def write_to_chat(arguments):
    host, port = arguments.host, arguments.port
    token, login = arguments.token, arguments.name

    if not token:
        logger.info('Токен не найден. Регистрация нового пользователя')
        async with open_connection(host, port) as conn:
            token = await sign_up(conn, login)
        logger.info(f'Регистрация под именем {login} завершена. Ваш токен {token}.')

        await write_token(token, path=TOKEN_PATH)

    async with open_connection(host, port) as conn:
        _, writer = conn
        try:
            await sign_in(conn, token)
        except InvalidTokenError:
            logger.error('Работа остановлена!!! Неизвестный токен, проверьте его или зарегистрируйте заново.')
            return

        message = arguments.message
        await submit_message(writer, message)


def main():
    load_dotenv()
    args = parse_args_write()
    asyncio.run(write_to_chat(args))


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

    main()
