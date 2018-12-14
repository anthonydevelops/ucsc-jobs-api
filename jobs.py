import requests
import re
from bs4 import BeautifulSoup


class Job:
    def __init__(self, link, date_posted, position, unit, pay):
        self.link = link
        self.date_posted = date_posted
        self.position = position
        self.unit = unit
        self.pay = pay


def scrapeLinks(links):
    urls = [[] for _ in range(2)]
    for idx, link in enumerate(links):
        link_req = requests.get(link)
        soup = BeautifulSoup(link_req.text, 'html.parser')

        # Gets all the url links to job postings
        href_tags = soup.find_all('a', href=re.compile('action=displayER'))
        for href_tag in href_tags:
            urls[idx].append(
                'http://www.careercenter.ucsc.edu/ers/erspub/' + href_tag.get('href'))

    return urls


def scrapeJobs(urls):
    jobs = [[] for _ in range(2)]
    for i in range(0, len(urls)):
        for idx, val in enumerate(urls[i]):
            url_req = requests.get(val)
            soup = BeautifulSoup(url_req.text, 'html.parser')

            # Gets position title
            position = soup.find('font', attrs={'face': 'verdana'})

            # Gets table titles
            table_title = soup.find_all('td', class_="title")
            subset_table_title = set(
                ['Computer', 'Filing', 'Driving', 'Other'])
            reqs_headers = [
                title for title in table_title if title not in subset_table_title]

            for header in reqs_headers:
                jobs[i].append(header.text)

            # Gets table descriptions
            reqs_desc = soup.find_all('td', class_="value")

    return jobs


if __name__ == '__main__':
    links = [
        'http://www.careercenter.ucsc.edu/ers/erspub/main.cfm?action=non_workstudy',
        'http://www.careercenter.ucsc.edu/ers/erspub/main.cfm?action=workstudy'
    ]

    urls = scrapeLinks(links)
    # print(urls)
    jobs = scrapeJobs(urls)
    print(jobs)
