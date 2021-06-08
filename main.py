from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def getlinkedinCount(tech, location):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
    driver.get(f'https://googleweblight.com/?lite_url=https://www.linkedin.com/jobs/search?keywords={tech}&location={location}')
    print(driver.page_source)
    count = driver.find_element_by_css_selector('#main-content > div > h1 > span.results-context-header__job-count').get_attribute('innerHTML')
    print(count)
    driver.close()
    return count

tech = 'splunk'
location = 'United States'

getlinkedinCount(tech, location)
