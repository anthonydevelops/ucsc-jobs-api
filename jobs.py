import requests
import re
from bs4 import BeautifulSoup


class Job:
    def __init__(self, link, date_posted, title, unit, pay):
        self.link = link
        self.date_posted = date_posted
        self.title = title
        self.unit = unit
        self.pay = pay


def scrapeLinks(links, urls):
    for link in links:
        req = requests.get(link)
        soup = BeautifulSoup(req.text, 'html.parser')

        # Gets all the url links to job postings
        href_tags = soup.find_all('a', href=re.compile('action=displayER'))
        for href_tag in href_tags:
            urls.append(
                'http://www.careercenter.ucsc.edu/ers/erspub/' + href_tag.get('href'))


def scrapeJobInfo(urls):
    for url in urls:
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')

        # Gets all job info


if __name__ == '__main__':
    links = [
        'http://www.careercenter.ucsc.edu/ers/erspub/main.cfm?action=non_workstudy',
        'http://www.careercenter.ucsc.edu/ers/erspub/main.cfm?action=workstudy'
    ]

    jobs = []
    urls = []
    scrapeLinks(links, urls)
    print(urls)
    # scrapeJobInfo(urls)
