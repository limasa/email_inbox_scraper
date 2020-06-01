from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from . import main_scraper, habitaclia_scraper


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(main_scraper.main_scraper, 'interval', seconds=10)
    scheduler.add_job(habitaclia_scraper.scrape_habitaclia,
                      'cron', second=25)
    scheduler.start()
