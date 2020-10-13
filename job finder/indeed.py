from gen_parse import BeautifulSoup
from gen_parse import get_page
from objects import job_c
from time import sleep
from random import randint

def get_jobs(soup):
    divs = soup.find_all('div')
    job_links = []
    for div in divs:
        try:
            #checks for the indicators of job postings
            if "pj_" in div.get("id") or "p_" in div.get("id"):     
                # makes a list of the links to the page that the job is on      
                job_links.append(div.find_all("a",href=True, class_="jobtitle turnstileLink")[0]["href"])
        except:
            pass

    return job_links

def get_next_page(soup):
    try:
        next = soup.find(attrs={"aria-label": "Next"})
        next = next["href"]
    except:
        next = False
    return(next)


def get_s_page_info(url):
        soup = get_page(url)
        jobs = get_jobs(soup)
        next_page = get_next_page(soup)

        return{"job_links": jobs, "next_page": next_page}
        

def add_prefix(url):
    return("https://ca.indeed.com" + url)


def parse_indeed(jobs):

    parsed_jobs = []

    for job in jobs:

        sleep(randint(10,100)/100)
        if "indeed.com" not in job:
            page = get_page(add_prefix(job))
        else:
            page = get_page(job)
        title = page.select(".icl-u-xs-mb--xs")[0].text
        parsed_job = job_c(title, add_prefix(job))

        try:
            company = page.select("div.icl-u-lg-mr--sm:nth-child(1)")[0].text
            parsed_job.company = company
        except:
            pass
        try:
            city = page.select(".jobsearch-InlineCompanyRating > div:nth-child(3)")[0].text
            parsed_job.city = city
        except:
            pass
        try:
            remote = page.select(".icl-u-textColor--secondary > div:nth-child(2)")[0].text
            if remote == "Remote":
                parsed_job.isremote = True
        except:
            pass
        try:
            salary = page.select("span.icl-u-xs-mr--xs")[0].text
            salary = salary.split()
            parsed_job.salary_low = salary[0][1:].replace(",","")
            parsed_job.salary_high = salary[2][1:].replace(",","")
        except:
            pass
        try:
            job_desc = page.select("#jobDescriptionText")[0].text
            parsed_job.description = job_desc
        except:
            pass
        
        parsed_jobs.append(parsed_job)
    return(parsed_jobs)


def search_indeed(term, city, country_code):
    term = term.replace(" ", "+")
    url = f"https://{country_code}.indeed.com/jobs?q={term}&l={city}"

    page_info = get_s_page_info(url)
    job_links = (page_info["job_links"])
    next_page = page_info["next_page"]

    while next_page:
        next_page = add_prefix(next_page)
        page_info = get_s_page_info(next_page)
        for link in page_info["job_links"]:
            job_links.append(link)
        next_page = page_info["next_page"]
    
    jobs = parse_indeed(job_links)
    return(jobs)
