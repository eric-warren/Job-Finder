from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os import listdir
from jinja2 import Environment, FileSystemLoader, select_autoescape


def getlinkedinCount(tech):

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
    driver.get(f'https://www.indeed.com/jobs?q={tech}&l=')
    count = driver.find_element_by_css_selector('#searchCountPages').get_attribute('innerHTML')
    count = int(count.strip()[10:-5].replace(',', ''))
    driver.close()
    return count

def getAllSearch():
    files = listdir('./searches')
    searches = {}
    for file in files:
        with open(f'./searches/{file}') as f:
            searches[file] = f.read().splitlines()
    return searches


def getAllCounts():
    searches = getAllSearch()
    allCounts = []
    for search in searches.items():
        res= {}
        for item in search[1]:
            res[item] = getlinkedinCount(item)

        allCounts.append([search[0], res])
    print(allCounts)
    return allCounts

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)
template = env.get_template("index.html")
temp = template.render(vars=getAllCounts())
with open('../index.html', 'w') as f:
    f.write(temp)
