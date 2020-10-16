from requests_html import HTMLSession
from bs4 import BeautifulSoup
from objects import job_c
import yaml

def get_parse_keys(settings):
    return settings["parse"]

def get_search_areas(settings):
    areas = []
    settings = settings["areas"]
    for area in settings.values():
        areas.append({"country_code":area["country_code"], "country":area["country"], "city":area["city"]})
    
    return areas

def get_search_keys(settings):
    search_keys = []
    settings = settings["search"]
    prefix, main_key, suffix, custom = settings["prefix"], settings["main_key"], settings["suffix"], settings["custom_search"]
    for key in custom:
        search_keys.append(key)

    for key in main_key:
        for end in suffix:
            search_keys.append(key + " " + end)
            for start in prefix:
                 search_keys.append(start + " " + key + " " + end)

def get_settings():
    with open('settings.yaml') as f:
        settings = yaml.load(f, Loader=yaml.FullLoader)
    
    updated_settings = {"parse_keys":get_parse_keys(settings), "areas":get_search_areas(settings), "search_keys":get_search_keys(settings)}

    return updated_settings



def get_page(url):
    session = HTMLSession()
    r = session.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse_desc(job):
    
    desc = job.description.lower()

    settings = get_settings()

    # Is ridiculous if statement sets the isremote parameter based off the keywoprds in the settings
    if job.isremote is None and any(key in desc for key in settings["parse_keys"]["remote"]["is"]) and not any(key in desc for key in settings["parse_keys"]["remote"]["not"]):\
        job.isremote = True

    if job.isremote is None and any(key in desc for key in settings["parse_keys"]["us_only"]["is"]) and not any(key in desc for key in settings["parse_keys"]["us_only"]["not"]):\
        job.isremote = True






f = open("demofile2.txt", "r")
job  = f.read().split("\n")

my_job = job_c(job[4], job[6] ,job[5])

my_job.description = job[0]
my_job.city = job[1]
my_job.salary_low = job[2]
my_job.salary_high = job[3]

parse_desc(my_job)