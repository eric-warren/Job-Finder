from requests_html import HTMLSession
from bs4 import BeautifulSoup
import yaml

def get_parse_keys(settings):
    """
    Getter for parse keys to make other code more readable

    Args:
        dict: dict with info from setting parsed bt pyyaml

    Returns:
        dict: dict of parse keys from settings
    """
    return settings["parse"]

def get_search_areas(settings):
    """
    Get the search areas form the setting

    Args:
        dict: dict with info from setting parsed bt pyyaml

    Returns:
        dict: dict of search areas from settings
    """
    areas = []
    settings = settings["areas"]
    for area in settings.values():
        areas.append({"country_code":area["country_code"], "country":area["country"], "city":area["city"]})
    
    return areas

def get_search_keys(settings):
    """
    Gets the search keys form the settings

    Args:
        dict: dict with info from setting parsed bt pyyaml

    Returns:
        dict: dict of search keys from settings
    """
    search_keys = []
    settings = settings["search"]

    # Gets the diffrent types of search keys
    prefix, main_key, suffix, custom = settings["prefix"], settings["main_key"], settings["suffix"], settings["custom_search"]

    # Add the custom search terms to the search list
    for key in custom:
        search_keys.append(key)

    # Add the follwoing combination to the search list (main_key + suffix), (prefix + main_key + suffix)
    for key in main_key:
        for end in suffix:
            search_keys.append(key + " " + end)
            for start in prefix:
                 search_keys.append(start + " " + key + " " + end)
    return search_keys

def get_settings():
    """
    Get and parses the infomation in th settings.yaml

    Returns:
        dict: all the setting for the program
    """

    # Open's the setting file and parses into a dict
    with open('settings.yaml') as f:
        settings = yaml.load(f, Loader=yaml.FullLoader)
    
    # Restructuring the dict
    updated_settings = {"parse_keys":get_parse_keys(settings), "areas":get_search_areas(settings), "search_keys":get_search_keys(settings)}

    return updated_settings



def get_page(url):
    """
    Gets a page that does not need to be rendered

    Args:
        url string: the url to get

    Returns:
        bs4 object of the page
    """
    session = HTMLSession()
    r = session.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    return soup

def parse_gen_job(job):
    """
    Parse's the doc and sets some of the attributes based off word in the description

    Args:
        job job_c object: job object found in object.py

    Returns:
        job_c object: job object found in object.py
    """
    # Set the description lowercase for easier parsing
    desc = job.description.lower()
    title = job.title.lower()

    settings = get_settings()

    # This ridiculous if statement sets the isremote parameter based off the keywords in the settings
    if job.isremote is False and any(key.lower() in desc for key in settings["parse_keys"]["remote"]["is"]) and not any(key.lower() in desc for key in settings["parse_keys"]["remote"]["not"]):
        job.isremote = True
    if job.isremote is False and any(key.lower() in title for key in settings["parse_keys"]["remote"]["is"]) and not any(key.lower() in title for key in settings["parse_keys"]["remote"]["not"]):
        job.isremote = True
    # Same as above except for us_only
    if job.us_only is False and any(key.lower() in desc for key in settings["parse_keys"]["us_only"]["is"]) and not any(key.lower() in desc for key in settings["parse_keys"]["us_only"]["not"]):
        job.us_only = True
    
    return job
