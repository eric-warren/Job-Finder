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

    sleep(randint(2,5)
    input_text(driver, "#sc\.keyword", term)
    sleep(randint(2,5)
    input_text(driver, "#sc\.location", city)
    sleep(randint(2,5)
    driver.find_element_by_css_selector("#HeroSearchButton").click()

def parse_glass_job(driver, job_link, city):
    
    driver.get(job_link)

    sleep(randint(5,10)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    company = soup.find("div", class_="css-16nw49e e11nt52q1").text
    title = soup.find("div", class_="css-17x2pwl e11nt52q6").text
    desc = soup.find("div", class_="desc css-58vpdc ecgq1xb4").text

    job = job_c(title, company, job_link, desc, city)

    return job
    


def parse_search(driver, city):

    job_links = []
    next_page = "first"
    x = 0
    while next_page:
        x += 1
        print(x)
        if next_page != "first":
            driver.find_element_by_css_selector(".next > a:nth-child(1)").click()
            
        wait_for_css(driver, ".jlGrid")

        try:
            wait_for_css(driver, ".modal_closeIcon-svg")
            driver.find_element_by_css_selector(".modal_closeIcon-svg").click()
        except:
            pass
        
        sleep(randint(2,5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        job_search_list = soup.find(class_="jlGrid hover p-0")

        job_search_list = job_search_list.find_all("li")

        for job in job_search_list:
            job_links.append("https://www.glassdoor.ca" + job.find_all("a",href=True, class_="css-10l5u4p e1n63ojh0 jobLink")[0]["href"])
        
        next_page = soup.find("a", {'data-test':'pagination-next'})

        try:
            next_page.find("span")["class"][0]
            next_page = False
        except:
            sleep(randint(5,10)
            next_page = 'next'
    
    return job_links
    
    


def search_glassdoor(term, city, country_code, country):

    url = "https://www.glassdoor.ca/ottawa"
    driver = webdriver.Firefox(executable_path=r'geckodriver.exe')

    driver.get(url)
    search_jobs(driver, term, city)

    job_links = parse_search()

    job_list = []

    for job_link in job_links:
        job = parse_glass_job(driver, job_link, city,)
        job.city = city
        job.country_code = country_code
        job.country = country
        job_list.append(parse_gen_job(job))
    return job_list




