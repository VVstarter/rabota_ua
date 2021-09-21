import asyncio
import logging
import time
from copy import deepcopy
from typing import Optional
from urllib.parse import urljoin

import requests
from fake_useragent import UserAgent
from parsel import Selector

from config import DOMAIN, HEADERS, PROXIES, SEARCH_QUERY, SEARCH_TOWN
from constants import (
    START_URL_CONTAINER,
    JOB_LINKS_XPATH,
    JOB_TITLE_XPATH,
    JOB_CONTACT_PERSON_XPATH,
    JOB_CONTACT_PHONE_NUMBER_XPATH,
)
from db.database import Database
from db.models import Job


class ScraperRabotaUaRequests:

    def __init__(self):
        self.database = Database()
        self.user_agent_randomizer: UserAgent = UserAgent()
        self.logger = logging.getLogger('RABOTA_UA')
        logging.basicConfig()
        self.logger.setLevel('INFO')

    async def _send_get_request(
            self,
            url: str,
            retry_count: int = 0,
    ) -> requests.Response:
        try:
            self.logger.info(f' Sending request to url: "{url}"...')
            return requests.get(
                url=url,
                headers=self._get_headers(),
                proxies=PROXIES,
                timeout=30,
                # verify=False,
            )
        except Exception as e:
            if retry_count < 3:
                return await self._send_get_request(
                    url=url,
                    retry_count=retry_count + 1,
                )
            else:
                self.logger.exception(e)

    async def start(self) -> None:
        await self._parse_pagination_page()

    async def _parse_pagination_page(
            self,
            page: int = 1,
    ) -> None:
        url = START_URL_CONTAINER.format(
            SEARCH_QUERY,
            SEARCH_TOWN,
            page,
        )

        for _ in range(3):
            page_response = await self._send_get_request(
                url=url,
            )

            if page_response.status_code == 200:
                break

            self.logger.info(f' Url: {url}. Response code: {page_response.status_code}. Retry...')
            time.sleep(2)
        else:
            self.logger.info(f' Url: {url}. Maximum retries exceeded')
            return

        pagination_page_tree = Selector(page_response.text)
        next_page_exists = await self._create_tasks_for_job_pages(
            pagination_page_tree=pagination_page_tree,
        )

        if not next_page_exists and page == 1:
            self.logger.info(
                f' Not found jobs using search query: "{SEARCH_QUERY}" and search_town: "{SEARCH_TOWN}"',
            )
        elif not next_page_exists:
            self.logger.info(f' Scraping process completed')
            return

        return await self._parse_pagination_page(
            page=page + 1,
        )

    async def _create_tasks_for_job_pages(
            self,
            pagination_page_tree: Selector,
    ) -> bool:
        job_pages_urls = pagination_page_tree.xpath(JOB_LINKS_XPATH).extract()

        if not job_pages_urls:
            return False

        tasks = []

        for job_page_url in job_pages_urls:
            task = asyncio.create_task(
                self._parse_job_page(
                    url=urljoin(
                        base=DOMAIN,
                        url=job_page_url,
                    ),
                )
            )
            tasks.append(task)

        await asyncio.gather(*tasks)
        tasks.clear()
        return True

    async def _parse_job_page(
            self,
            url: str,
    ) -> None:
        for _ in range(3):
            job_page_response = await self._send_get_request(
                url=url,
            )

            if job_page_response.status_code == 200:
                break

            self.logger.info(f' Url: {url}. Response code: {job_page_response.status_code}. Retry...')
        else:
            self.logger.info(f' Url: {url}. Maximum retries exceeded')
            return

        job_page_tree = Selector(job_page_response.text)
        job_data = dict()
        job_data['url'] = job_page_response.url.split('?')[0]
        job_data['city'] = SEARCH_TOWN
        job_data['title'] = await self.parse_job_title(
            job_page_tree=job_page_tree,
        )
        job_data['contact_person'] = await self.parse_job_contact_person(
            job_page_tree=job_page_tree,
        )
        job_data['contact_phone_numbers'] = await self.parse_job_phone_numbers(
            job_page_tree=job_page_tree,
        )
        self.save_job(job_data=job_data)

    def save_job(
            self,
            job_data: dict,
    ) -> None:
        job = Job(
            url=job_data['url'],
            city=job_data['city'],
            title=job_data['title'],
            contact_person=job_data['contact_person'],
            contact_numbers=job_data['contact_phone_numbers'],
        )
        self.database.add_job(
            job=job,
        )

    def _get_headers(
            self,
    ) -> dict:
        headers = deepcopy(HEADERS)
        headers['user-agent'] = self.user_agent_randomizer.random
        return headers

    @staticmethod
    async def parse_job_title(
            job_page_tree: Selector,
    ) -> str:
        return job_page_tree.xpath(JOB_TITLE_XPATH).extract_first()

    @staticmethod
    async def parse_job_contact_person(
            job_page_tree: Selector,
    ) -> Optional[str]:
        return job_page_tree.xpath(JOB_CONTACT_PERSON_XPATH).extract_first()

    @staticmethod
    async def parse_job_phone_numbers(
            job_page_tree: Selector,
    ) -> Optional[list]:
        string_with_phone_numbers = job_page_tree.xpath(JOB_CONTACT_PHONE_NUMBER_XPATH).extract_first()

        if string_with_phone_numbers:
            phone_numbers = string_with_phone_numbers \
                .replace(',', '+') \
                .strip('+') \
                .split('+')
            phone_numbers = [
                entry.strip()
                    .replace('-', '')
                    .replace('(', '')
                    .replace(')', '')
                for entry in phone_numbers if entry.strip()
            ]
            phone_numbers = list(set(phone_numbers))
            return phone_numbers
