import argparse
import asyncio
import logging

from aiopath import AsyncPath
from aioshutil import copyfile


# асинхронна функція для рекурсивного читання файлів з папки
async def read_folder(path: AsyncPath) -> None:
    try:
        async for file in path.iterdir():
            if await file.is_file():
                await copy_file(file)
            elif await file.is_dir():
                await read_folder(file)
    except Exception as e:
        logging.error(f"Error reading folder {path}: {e}")


# асинхронна функція для копіювання файлу
async def copy_file(file: AsyncPath) -> None:
    try:
        extension_name = file.suffix[1:]
        extension_folder = output / extension_name
        await extension_folder.mkdir(exist_ok=True, parents=True)
        await copyfile(file, extension_folder / file.name)
        logging.info(
            f"File {file.name} copied successfully to {extension_folder}")
    except PermissionError as e:
        logging.error(f"Permission denied while copying file {file}: {e}")
    except Exception as e:
        logging.error(f"Failed to copy file {file}: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] - %(message)s")

    # створення парсера аргументів
    parser = argparse.ArgumentParser(
        description="Copy files based on their extension")
    parser.add_argument("source", type=str, help="Source folder")
    parser.add_argument("output", type=str, help="Output folder")

    # парсимо аргументи
    args = parser.parse_args()

    # створення шляхів
    source = AsyncPath(args.source)
    output = AsyncPath(args.output)

    # запуск асинхронного процесу
    asyncio.run(read_folder(source))
