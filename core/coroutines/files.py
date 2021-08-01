import aiofiles


async def write_token(token: str, path):
    """
    Запись токена в файл.

    :param token: Токен
    :param path: Путь до файла (Если его нет то создастся)
    """
    async with aiofiles.open(path, 'w', encoding='utf-8') as f:
        await f.write(f'token = {token}')
