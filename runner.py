import asyncio


async def read_chat():
    while True:
        reader, _ = await asyncio.open_connection('minechat.dvmn.org', 5000)
        data = await reader.read(100)
        print(f'{data.decode()!r}')


if __name__ == '__main__':
    asyncio.run(read_chat())
