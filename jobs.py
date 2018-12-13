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


def scrapeLinks(links, urls):
    for link in links:
        link_req = requests.get(link)
        soup = BeautifulSoup(link_req.text, 'html.parser')

        # Gets all the url links to job postings
        href_tags = soup.find_all('a', href=re.compile('action=displayER'))
        for href_tag in href_tags:
            urls.append(
                'http://www.careercenter.ucsc.edu/ers/erspub/' + href_tag.get('href'))


def scrapeJobInfo(info, urls):
    for url in urls:
        url_req = requests.get(url)
        soup = BeautifulSoup(url_req.text, 'html.parser')

        # Gets all job info
        position = soup.find('font', attrs={'face': 'verdana'})
        reqs_title = soup.find_all('td', class_="title")
        reqs_desc = soup.find_all('td', class_="value")


if __name__ == '__main__':
    links = [
        'http://www.careercenter.ucsc.edu/ers/erspub/main.cfm?action=non_workstudy',
        'http://www.careercenter.ucsc.edu/ers/erspub/main.cfm?action=workstudy'
    ]

    jobs = []
    urls = []
    info = []
    scrapeLinks(links, urls)
    scrapeJobInfo(info, urls)
