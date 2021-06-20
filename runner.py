import asyncio
import datetime

import aiofiles


async def read_chat():
    while True:
        reader, _ = await asyncio.open_connection('minechat.dvmn.org', 5000)
        data = await reader.read(100)

        message_text = data.decode()
        message_time = datetime.datetime.now().strftime('[%d.%m.%y %H:%M]')
        message = message_time + ' ' + message_text

        async with aiofiles.open('chatlog.txt', mode='a', encoding='utf-8') as f:
            await f.write(message)
        print(f'{message}')


if __name__ == '__main__':
    asyncio.run(read_chat())
