import hashlib 

class job_c:

    isremote = None
    company = None
    description = None
    city = None
    salary_low = None
    salary_high = None
    us_only = None
    md5 = None

    def __init__(self, title, company ,url):
        self.title = title
        self.company = company
        self.url = url
        self.hash = hashlib.md5((title+company.name).encode()) 


class company_c:

    def __init__(self, name,):
        self.name = name