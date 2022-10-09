import schedule
import time
import datetime
import crawler

def crawler_job():
    date = datetime.datetime.now()
    print(date)
    print(f"Running at: {date.day}/{date.month}/{date.year} ({date.hour}:{date.minute})\n")
    crawler.run_crawler()

schedule.every().monday.at("03:00").do(crawler_job)
# schedule.every(10).seconds.do(crawler_job)

while True:
    schedule.run_pending()
    time.sleep(1)