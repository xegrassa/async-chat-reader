import asyncio
import datetime
import os
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


async def write_to_chat(host, port):
    token = os.getenv('TOKEN')
    reader, writer = await asyncio.open_connection(host, port)

    writer.write(token.encode() + b'\n')
    await writer.drain()

    writer.write(b'Hello Chat !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n')
    await writer.drain()
    writer.close()


if __name__ == '__main__':
    load_dotenv()
    args = parse_args()
    print(args)

    # asyncio.run(read_chat(args.host, args.port, args.history))
    asyncio.run(write_to_chat(args.host, 5050))
