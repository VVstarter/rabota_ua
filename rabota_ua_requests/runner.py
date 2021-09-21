from rabota_ua_requests import ScraperRabotaUaRequests
import asyncio


if __name__ == '__main__':
    scraper = ScraperRabotaUaRequests()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scraper.start())
