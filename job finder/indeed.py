from gen_parse import get_page
from gen_parse import parse_gen_job
from objects import job_c
from time import sleep
from random import randint

def get_job_links(soup):
    """
    finds all the job posting in the search page of indeed

    Args:
        soup bs4 object: page that was scraped

    Returns:
        list: list of the links to all the jobn postings
    """
    divs = soup.find_all('div')
    job_links = []
    for div in divs:
        try:
            # Checks for the indicators of job postings
            if "pj_" in div.get("id") or "p_" in div.get("id"):     
                # Makes a list of the links to the page that the job is on      
                job_links.append(div.find_all("a",href=True, class_="jobtitle turnstileLink")[0]["href"])
        except:
            pass

    return job_links

def get_next_page(soup):
    """
    Gets the next page link if it exists

    Args:
        soup bs4 object: page that was scraped

    Returns:
        string: link to next page
    """
    try:
        # Gets the link to the next page
        next = soup.find(attrs={"aria-label": "Next"})
        next = next["href"]
    except:
        # If its the last page ste the next page to false
        next = False
    return next


def get_s_page_info(url):
    """
    Gets the search page and all the needed info about it

    Args:
        url string: the url of the search
    """
    # Gets the page
    soup = get_page(url)

    # Gets the job links
    jobs = get_job_links(soup)

    # Get the link to the next page
    next_page = get_next_page(soup)

    return{"job_links": jobs, "next_page": next_page}
        

def add_prefix(url, country_code):
    """
    adds the proper prefix to the indeed url

    Args:
        url string: URL with proper subdomain
    """
    url = "https://%s.indeed.com" % (country_code) + url

    return(url)


def parse_indeed(jobs, country_code):
    """[summary]

    Args:
        jobs list: job links that need to be parsed
        country_code string: country code for the indeed subdomain

    Returns:
        list: job objects that have all the info parsed
    """

    parsed_jobs = []

    # Loops through job links
    for job in jobs:

        #random delay might move this later
        sleep(randint(5, 10))
        
        # checks if the prefix is already in the link if nto adds it
        if "indeed.com" not in job:
            page = get_page(add_prefix(job, country_code))
        else:
            page = get_page(job)
        
        # Grabs the job title and company from the page (some links go directly to the company page therefore a try continue)
        try:
            title = page.select(".icl-u-xs-mb--xs")[0].text
            company = page.select("div.icl-u-lg-mr--sm:nth-child(1)")[0].text

        except:
            continue

        parsed_job = job_c(title, company ,add_prefix(job, country_code))


        # Tries to get the city from the page
        try:
            city = page.select(".jobsearch-InlineCompanyRating > div:nth-child(3)")[0].text
            parsed_job.city = city
        except:
            pass

        # Tries to get if the job is remote from the page
        try:
            remote = page.select(".icl-u-textColor--secondary > div:nth-child(2)")[0].text
            if remote == "Remote":
                parsed_job.isremote = True
        except:
            pass

        # Tries to get the salary range from the page
        try:
            salary = page.select("span.icl-u-xs-mr--xs")[0].text
            salary = salary.split()
            parsed_job.salary_low = salary[0][1:].replace(",","")
            parsed_job.salary_high = salary[2][1:].replace(",","")
        except:
            pass

        # Tries to get the job description from the page
        try:
            job_desc = page.select("#jobDescriptionText")[0].text
            parsed_job.description = job_desc
        except:
            pass
        
        # Adds the job to the parsed list
        parsed_jobs.append(parsed_job)

    return parsed_jobs


def search_indeed(term, city, country_code, country):
    """
    Main Indeed function that call all the other functions and creates the search url

    Args:
        term string: what you want to search on indeed
        city string: what city you want to search
        country_code string: the country code to search

    Returns:
        [type]: [description]
    """
    # Creates the search url
    term = term.replace(" ", "+")
    url = f"https://{country_code}.indeed.com/jobs?q={term}&l={city}"

    # Get all the iunfo about the search results page
    page_info = get_s_page_info(url)

    # Gets the list and string from the dict that was returned
    job_links = (page_info["job_links"])
    next_page = page_info["next_page"]

    # While therte is still a next page go to it and get all the info
    while next_page:
        sleep(2.5)
        next_page = add_prefix(next_page, country_code)
        page_info = get_s_page_info(next_page)
        for link in page_info["job_links"]:
            job_links.append(link)
        next_page = page_info["next_page"]
    
    # Parses the job to create job objects
    jobs = parse_indeed(job_links, country_code)

    parsed_jobs = []

    for job in jobs:
        job = parse_gen_job(job)
        job.city = city
        job.country_code = country_code
        job.country = country
        parsed_jobs.append(job)

    return parsed_jobs
