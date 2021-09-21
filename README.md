Run rabota_ua_scrapy:
    1. open root directory in terminal
    2. write the command "cd rabota_ua_scrapy"
    3. Set the environment variables in the docker-compose.yml:
        a) SEARCH_QUERY = desired search query (e.g. junior python developer) 
            to search on rabota.ua
        b) SEARCH_TOWN - desired city to search on rabota.ua
    3. write the command "docker-compose up --build -d"
    4. the script will save all found vacancies to the database

Run rabota_ua_requests:
    1. open root directory in terminal
    2. write the command "cd rabota_ua_requests"
    3. Set the environment variables in the docker-compose.yml:
        a) SEARCH_QUERY = desired search query (e.g. junior python developer) 
            to search on rabota.ua
        b) SEARCH_TOWN - desired city to search on rabota.ua
        c) PROXIES - proxies that will be used in requests
    3. write the command "docker-compose up --build -d"
    4. the script will save all found vacancies to the database