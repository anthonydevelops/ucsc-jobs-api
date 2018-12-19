import requests
import re
import json
from bs4 import BeautifulSoup


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
            desc = []

            # Gets position title
            position = soup.find('font', attrs={'face': 'verdana'})

            # Gets table descriptions
            table_desc = soup.find_all('td', class_="value")
            for d_idx, d_val in enumerate(table_desc):
                if (d_idx < 8) or (d_idx == len(table_desc)-1):
                    desc.append(d_val.text.strip())

            # Connect headers to desc, in JSON form
            jobs[i].append({
                "title": position.text.strip(),
                "unit": desc[0],
                "pay": desc[1],
                "filingdate": desc[2],
                "employmentdate": desc[3],
                "hours": desc[4],
                "schedule": desc[5],
                "skillsreq": desc[6],
                "skillspref": desc[7],
                "dateapproved": desc[8]
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
        json.dump(jobs, outfile, sort_keys=True, indent=4)
