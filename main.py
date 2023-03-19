import pandas as pd
from loguru import logger
from campsite import crawl_camping_info
from datetime import datetime, timedelta, timezone

if __name__ == '__main__':
    logger.add("camping.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")
    day = datetime.today().day
    if day == 1:
        campsite_info = crawl_camping_info.CrawlCampsiteInfo()
        campsite_info.Crawl_CampSite()
    else:
        


