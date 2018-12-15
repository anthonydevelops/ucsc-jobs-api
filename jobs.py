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

    # Cycle through work-study/non-work-study
    for i in range(0, len(urls)):

        # For each url, parse that page and save it as a job
        # based off the index
        for val in urls[i]:
            url_req = requests.get(val)
            soup = BeautifulSoup(url_req.text, 'html.parser')

            # Gets position title
            position = soup.find('font', attrs={'face': 'verdana'})
            position = position.text.strip()

            # Gets table titles
            table_title = soup.find_all('td', class_="title")
            for t_idx, t_val in enumerate(table_title):
                if (t_idx < 9) or (t_idx == table_title[-1]):
                    jobs[i].append(t_val.text)

            # Gets table descriptions
            table_desc = soup.find_all('td', class_="value")
            for d_idx, d_val in enumerate(table_desc):
                if d_idx < 9:
                    jobs[i].append(d_val.text)
                else:
                    break

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
