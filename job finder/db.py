from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import database_exists, create_database

if not database_exists("sqlite:///job_db.db"):
    create_database("sqlite:///job_db.db")
engine = create_engine("sqlite:///job_db.db")

session = sessionmaker(bind=engine)()

base = declarative_base()

class db_job(base):
    
    __tablename__ = "jobs"

    md5 = Column(String, primary_key=True)
    isremote = Column(Boolean)
    company = Column(Integer, ForeignKey('companies.name'))
    description = Column(String)
    city = Column(String)
    salary_low = Column(Integer)
    salary_high = Column(Integer)
    us_only = Column(Boolean)

class db_company(base):

    __tablename__ = "companies"

    name = Column(String, primary_key=True)
    job = relationship("jobs")


from objects import job_c
from objects import company_c

job = job_c("title",company_c("company"), "https://")
company = company_c("company")

session.add(db_company(company))
session.add(db_job(job))
session.commit