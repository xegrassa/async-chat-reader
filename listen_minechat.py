import asyncio
import datetime
from pathlib import Path

import aiofiles
from dotenv import load_dotenv

from core.cli import parse_args_listen
from core.coroutines import open_connection


async def read_chat(host, port, history):
    async with open_connection(host, port) as conn:
        reader, _ = conn
        while True:
            data = await reader.readuntil(b'\n')

            message_text = data.decode()
            message_time = datetime.datetime.now().strftime('[%d.%m.%y %H:%M]')
            message = f'{message_time} {message_text}'

            async with aiofiles.open(history, mode='a', encoding='utf-8') as f:
                await f.write(message)
            print(message)


if __name__ == '__main__':
    load_dotenv()
    args = parse_args_listen()
    try:
        asyncio.run(read_chat(args.host, args.port, args.history))
    except KeyboardInterrupt:
        print(f'Конец работы скрипта. Лог переписки в {Path().cwd() / args.history}')
