from selenium import webdriver
from selenium.webdriver.chrome.options import Options

tech = 'splunk'
location = 'United States'

def getlinkedinCount(tech, location):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
    driver.get(f'https://www.linkedin.com/jobs/search?keywords={tech}&location={location}')

    count = driver.find_element_by_css_selector('#main-content > div > h1 > span.results-context-header__job-count').get_attribute('innerHTML')
    print(count)
    driver.close()
    return count
