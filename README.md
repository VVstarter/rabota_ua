Usage rabota_ua_scrapy
-----

1. open root directory in terminal
2. write the command:
```
cd rabota_ua_scrapy
```
3. Set the environment variables in the docker-compose.yml:

    `SEARCH_QUERY` = desired search query (e.g. junior python developer) 
            to search on rabota.ua

    `SEARCH_TOWN` - desired city to search on rabota.ua

4. Write the command:
```
docker-compose up --build -d
```
5. The script will save all found vacancies to the database

Usage rabota_ua_requests
-----

1. open root directory in terminal
2. write the command:
```
cd rabota_ua_requests
```
3. Set the environment variables in the docker-compose.yml:

    `SEARCH_QUERY` = desired search query (e.g. junior python developer) 
            to search on rabota.ua

    `SEARCH_TOWN` - desired city to search on rabota.ua

    `PROXIES` - proxies that will be used in requests

4. Write the command:
```
docker-compose up --build -d
```
5. The script will save all found vacancies to the database