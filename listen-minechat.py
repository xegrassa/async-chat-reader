import asyncio
import datetime

import aiofiles
from dotenv import load_dotenv

from cli import parse_args


async def read_chat(host, port, history):
    while True:
        reader, _ = await asyncio.open_connection(host, port)
        data = await reader.read(100)

        message_text = data.decode()
        message_time = datetime.datetime.now().strftime('[%d.%m.%y %H:%M]')
        message = message_time + ' ' + message_text

        async with aiofiles.open(history, mode='a', encoding='utf-8') as f:
            await f.write(message)
        print(f'{message}')


if __name__ == '__main__':
    load_dotenv()
    args = parse_args()

    asyncio.run(read_chat(args.host, args.port, args.history))
