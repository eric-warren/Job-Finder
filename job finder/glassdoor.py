from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from objects import job_c
from gen_parse import parse_gen_job
from db import get_jobs

def wait_for_css(driver, css):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, css))
        )
    except:
        pass


def input_text(driver, selector, inp):

    inputElement = driver.find_element_by_css_selector(selector)
    inputElement.send_keys(inp)

def search_jobs(driver, term, city):
    input_text(driver, "#sc\.keyword", term)
    sleep(randint(1,2))
    input_text(driver, "#sc\.location", city)
    sleep(randint(1,2))
    driver.find_element_by_css_selector("#HeroSearchButton").click()

def parse_glass_job(driver, job, city):
    
    driver.get(job.url)

    sleep(randint(3,6))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    desc = soup.find("div", class_="desc css-58vpdc ecgq1xb4").text

    job.description = desc

    return job
    


def parse_search(driver, city):

    jobs = []
    next_page = "first"

    while next_page:
        if next_page != "first":
            driver.find_element_by_css_selector(".next > a:nth-child(1)").click()
            
        wait_for_css(driver, ".jlGrid")

        try:
            wait_for_css(driver, ".modal_closeIcon-svg")
            driver.find_element_by_css_selector(".modal_closeIcon-svg").click()
        except:
            pass
        

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        job_search_list = soup.find(class_="jlGrid hover p-0")

        job_search_list = job_search_list.find_all("li")

        for job in job_search_list:
            url = "https://www.glassdoor.ca" + job.find_all("a",href=True, class_="css-10l5u4p e1n63ojh0 jobLink")[0]["href"]
            company = job.find("a", class_="css-10l5u4p e1n63ojh0 jobLink").text
            title = job.find("a", class_="jobInfoItem jobTitle css-13w0lq6 eigr9kq1 jobLink").text
            jobs.append(job_c(title, company, url))
        
        next_page = soup.find("a", {'data-test':'pagination-next'})

        try:
            next_page.find("span")["class"][0]
            next_page = False
        except:
            next_page = 'next'
    
    return jobs
    
    


def search_glassdoor(term, city, country_code, country):

    url = "https://www.glassdoor.ca/ottawa"
    driver = webdriver.Firefox(executable_path=r'geckodriver.exe')

    driver.get(url)
    search_jobs(driver, term, city)

    jobs = parse_search(driver, city)

    job_list = []

    for job in jobs:
        current_jobs = get_jobs()
        used_md5 = []
        for c_job in current_jobs:
            used_md5.append(c_job.md5)
        
        if job.md5 in used_md5:
            continue
        job = parse_glass_job(driver, job, city,)
        job.city = city
        job.country_code = country_code
        job.country = country
        job_list.append(parse_gen_job(job))
    return job_list


t = search_glassdoor("network engineer", "ottawa", "a", "a")
print(type(t))
print(t)
print(len(t))
