import requests
import re
from bs4 import BeautifulSoup

links = [
    'http://www.careercenter.ucsc.edu/ers/erspub/main.cfm?action=non_workstudy',
    'http://www.careercenter.ucsc.edu/ers/erspub/main.cfm?action=workstudy'
]

jobs = []


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

    job_list = soup.find_all('td', class_='smallwording')
    for job in job_list:
        title = job.contents[0]
        print(title)
