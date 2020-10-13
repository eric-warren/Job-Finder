from requests_html import HTMLSession
from bs4 import BeautifulSoup
from objects import job_c

def get_page(url):
    session = HTMLSession()
    r = session.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse_desc(job):
    
    desc = job.description.lower()
    if job.isremote is not None:



f = open("demofile2.txt", "r")
job  = f.read().split("\n")

my_job = job_c(job[4], job[5])

my_job.company = job[6]
my_job.description = job[0]
my_job.city = job[1]
my_job.salary_low = job[2]
my_job.salary_high = job[3]

parse_desc(my_job)