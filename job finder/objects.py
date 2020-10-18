import hashlib 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean

base = declarative_base()

class job_c(base):

    __tablename__ = "jobs"

    md5 = Column(String, primary_key=True)
    isremote = Column(Boolean)
    company = Column(String)
    description = Column(String)
    city = Column(String)
    salary_low = Column(Integer)
    salary_high = Column(Integer)
    us_only = Column(Boolean)

    def __init__(self, title, company, url, description = "none", city = "none", isremote = False, salary_low = 0, salary_high = 0, us_only = False, md5 = "None"):
        self.title = title
        try:
            self.company = company.name
        except:
            self.company = company
        self.url = url
        if md5 is not "None":
            self.md5 = md5
        else:
            self.md5 = hashlib.md5((title+company).encode()) 
        self.isremote = isremote
        self.description = description
        self.city = city
        self.salary_low = salary_low
        self.salary_high = salary_high
        self.us_only = us_only


class company_c:

    __tablename__ = "companies"

    name = Column(String, primary_key=True)

    def __init__(self, name):
        self.name = name