# xpath's
NEXT_PAGE_XPATH = './/a[@rel="next" and contains(@href, "zapros/job")]/@href'
JOB_LINKS_XPATH = '//h2[@class="card-title"]/a/@href'
JOB_TITLE_XPATH = './/h1[contains(@class, "vacancy") and contains(@class, "title")]/text()'
JOB_CONTACT_PERSON_XPATH = './/div[contains(@class, contact-item)]/span[contains(text(), "Контакт")]' \
                           '/following-sibling::span/text()'
JOB_CONTACT_PHONE_NUMBER_XPATH = './/div[contains(@class, contact-item)]/span[contains(text(), "Телефон")]' \
                                 '/following-sibling::span/text()'
