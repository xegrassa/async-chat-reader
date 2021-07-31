import logging
from asyncio import StreamWriter, StreamReader

logger = logging.getLogger(__name__)


async def submit_message(writer: StreamWriter, message: str = ''):
    send_message = message.replace('\n', '')
    logger.debug(send_message)
    writer.write((send_message + '\n\n').encode())
    await writer.drain()


async def read_message(reader: StreamReader) -> str:
    response = await reader.readline()
    logger.debug(response.decode())
    return response.decode()
