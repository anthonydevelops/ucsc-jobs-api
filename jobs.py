import requests
import re
from bs4 import BeautifulSoup

links = [
    'http://www.careercenter.ucsc.edu/ers/erspub/main.cfm?action=non_workstudy',
    'http://www.careercenter.ucsc.edu/ers/erspub/main.cfm?action=workstudy'
]

jobs = []
urls = []


class Job:
    def __init__(self, link, date_posted, title, unit, pay):
        self.link = link
        self.date_posted = date_posted
        self.title = title
        self.unit = unit
        self.pay = pay


for link in links:
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'html.parser')

    # Gets the excerpt of the job posting
    job_list = soup.find_all('td', class_="smallwording")

    # Gets all the url links to job postings
    href_tags = soup.find_all('a', href=re.compile('action=displayER'))
    for href_tag in href_tags:
        urls.append(
            'http://www.careercenter.ucsc.edu/ers/erspub/' + href_tag.get('href'))

    # Cycles through job excerpt to parse info in chunks
    for job in job_list:
        listing = job.contents[0]

print(urls)
