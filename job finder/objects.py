import hashlib 

class job_c:

    isremote = False
    description = "None"
    city = "None"
    salary_low = 0
    salary_high = 0
    us_only = False
    md5 = "None"

    def __init__(self, title, company ,url):
        self.title = title
        self.company = company.name
        self.url = url
        self.hash = hashlib.md5((title+company.name).encode()) 


class company_c:

    def __init__(self, name):
        self.name = name