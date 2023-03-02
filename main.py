import pandas as pd
from loguru import logger


if __name__ == '__main__':
    logger.add("camping.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")
