from loguru import logger

logger.add("test.log", format="{time} {level} {message}", level="ERROR")
if __name__ == '__main__':
    10 / 0
