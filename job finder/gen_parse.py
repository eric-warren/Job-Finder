from requests_html import HTMLSession
from bs4 import BeautifulSoup

def get_page(url):
    session = HTMLSession()
    r = session.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup
