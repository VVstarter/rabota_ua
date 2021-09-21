import logging
from copy import deepcopy
from typing import Optional
from urllib.parse import urljoin

from fake_useragent import UserAgent
from scrapy import Spider, Request
from scrapy.http.response.html import HtmlResponse

from ..config import DOMAIN, START_URL, HEADERS, SEARCH_TOWN
from ..constants import (
    NEXT_PAGE_XPATH,
    JOB_TITLE_XPATH,
    JOB_LINKS_XPATH,
    JOB_CONTACT_PERSON_XPATH,
    JOB_CONTACT_PHONE_NUMBER_XPATH,
)
from ..db.database import Database
from ..db.models import Job

logging.getLogger('scrapy').setLevel(logging.WARNING)


class RabotaUaSpider(Spider):
    name = 'rabota_ua'
    allowed_domains = ['rabota.ua']
    database: Database = Database()
    user_agent_randomizer: UserAgent = UserAgent()

    def start_requests(
            self,
    ) -> None:
        headers = self._get_headers()
        request = Request(
            url=START_URL,
            callback=self.parse_page,
            headers=headers,
        )
        yield request

    def parse_page(
            self,
            response: HtmlResponse,
    ) -> None:
        next_page = response.xpath(NEXT_PAGE_XPATH).extract_first()

        for job_link in response.xpath(JOB_LINKS_XPATH).extract():
            request = Request(
                url=urljoin(
                    base=DOMAIN,
                    url=job_link,
                ),
                callback=self.parse_job_post,
                headers=HEADERS,
            )
            yield request

        if next_page:
            request = Request(
                url=urljoin(
                    base=DOMAIN,
                    url=next_page,
                ),
                callback=self.parse_page,
                headers=HEADERS,
            )
            yield request

    def parse_job_post(
            self,
            response: HtmlResponse,
    ) -> None:
        job_data = dict()
        job_data['url'] = response.url.split('?')[0]
        job_data['city'] = SEARCH_TOWN
        job_data['title'] = self.parse_job_title(
            response=response,
        )
        job_data['contact_person'] = self.parse_job_contact_person(
            response=response,
        )
        job_data['contact_phone_numbers'] = self.parse_job_phone_numbers(
            response=response,
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
    def parse_job_title(
            response: HtmlResponse,
    ) -> str:
        return response.xpath(JOB_TITLE_XPATH).extract_first()

    @staticmethod
    def parse_job_contact_person(
            response: HtmlResponse,
    ) -> Optional[str]:
        # maybe there might be several contact persons, but i don't have enough time to research
        return response.xpath(JOB_CONTACT_PERSON_XPATH).extract_first()

    @staticmethod
    def parse_job_phone_numbers(
            response: HtmlResponse,
    ) -> Optional[list]:
        # maybe there might be different cases, but i don't have enough time to research
        string_with_phone_numbers = response.xpath(JOB_CONTACT_PHONE_NUMBER_XPATH).extract_first()

        if string_with_phone_numbers:
            phone_numbers = string_with_phone_numbers\
                .replace(',', '+')\
                .strip('+')\
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
