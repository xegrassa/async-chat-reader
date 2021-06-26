import asyncio
import logging
import os
import json
from dotenv import load_dotenv

from cli import parse_args
from core.logging import configure_logging


async def write_to_chat(host, port, token):
    logger = logging.getLogger('writer-minechar')
    reader, writer = await asyncio.open_connection(host, port)

    data = await reader.readline()
    logger.debug(data.decode())

    message = token.encode() + b'\n'
    writer.write(message)
    logger.debug(message)
    await writer.drain()

    data = await reader.readline()
    if json.loads(data) is None:
        print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
        return
    logger.debug(data.decode())
    data = await reader.readline()
    logger.debug(data.decode())

    message = b'Hello Chat !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n'
    writer.write(message)
    logger.debug(message)
    await writer.drain()
    writer.close()


if __name__ == '__main__':
    configure_logging('writer-minechar')
    load_dotenv()
    args = parse_args()
    token = os.getenv('TOKEN')

    asyncio.run(write_to_chat(args.host, 5050, token))
