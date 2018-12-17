import requests
import re
import json
from bs4 import BeautifulSoup


class Job:
    def __init__(self, link, date_posted, position, unit, pay):
        self.link = link
        self.position = position
        self.date_posted = date_posted
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
        for val in urls[i]:
            url_req = requests.get(val)
            soup = BeautifulSoup(url_req.text, 'html.parser')

            # Declare parsed content arrays
            headers = []
            desc = []

            # Gets position title
            position = soup.find('font', attrs={'face': 'verdana'})

            # Gets table titles
            table_title = soup.find_all('td', class_="title")
            for t_idx, t_val in enumerate(table_title):
                if (t_idx < 8) or (t_val == table_title[-1]):
                    headers.append(t_val.text.strip())

            # Gets table descriptions
            table_desc = soup.find_all('td', class_="value")
            for d_idx, d_val in enumerate(table_desc):
                if (d_idx < 8) or (d_val == table_desc[-1]):
                    desc.append(d_val.text.strip())

            # Connect headers to desc, in JSON form
            jobs[i].append({
                "title": position.text.strip(),
                headers[0]: desc[0],
                headers[1]: desc[1],
                headers[2]: desc[2],
                headers[3]: desc[3],
                headers[4]: desc[4],
                headers[5]: desc[5],
                headers[6]: desc[6],
                headers[7]: desc[7],
            })

    return jobs


if __name__ == '__main__':
    links = [
        'http://www.careercenter.ucsc.edu/ers/erspub/main.cfm?action=non_workstudy',
        'http://www.careercenter.ucsc.edu/ers/erspub/main.cfm?action=workstudy'
    ]

    urls = scrapeLinks(links)
    jobs = scrapeJobs(urls)
    with open('data.json', 'w') as outfile:
        json.dump(jobs, outfile)
