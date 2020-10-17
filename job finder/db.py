from sqlalchemy import create_engine , Column , Boolean, String, Integer, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


def create_db():
    if not database_exists("sqlite:///job_db.db"):
        create_database("sqlite:///job_db.db")
    engine = create_engine("sqlite:///job_db.db")

    if not engine.dialect.has_table(engine, "jobs"):  # If table don't exist, Create.
        metadata = MetaData(engine)
        # Create a table with the appropriate Columns
        Table("jobs", metadata,
            Column('md5', String, primary_key=True), 
            Column('isremote', Boolean), Column('company', String),
            Column('description', String), Column('city', String),
            Column('salary_low', Integer), Column('salary_high', Integer),
            Column('us_only', Boolean))
        # Implement the creation
        metadata.create_all()

    if not engine.dialect.has_table(engine, "companies"):  # If table don't exist, Create.
        metadata = MetaData(engine)
        # Create a table with the appropriate Columns
        Table("companies", metadata,
            Column('name', String, primary_key=True))
        # Implement the creation
        metadata.create_all()


base = declarative_base()

class db_job(base):
    
    __tablename__ = "jobs"

    md5 = Column(String, primary_key=True)
    isremote = Column(Boolean)
    company = Column(String)
    description = Column(String)
    city = Column(String)
    salary_low = Column(Integer)
    salary_high = Column(Integer)
    us_only = Column(Boolean)

    def __init__(self, job):
        self.md5 = job.md5
        self.isremote = job.isremote
        self.company = job.company
        self.description = job.description
        self.city = job.city
        self.salary_low = job.salary_low
        self.salary_high = job.salary_high
        self.us_only = job.us_only

class db_company(base):

    __tablename__ = "companies"

    name = Column(String, primary_key=True)

    def __init__(self, comp):
        self.name = comp.name

def insert_job(job):
    all_jobs = get_jobs()

    if job not in all_jobs:

        engine = create_engine("sqlite:///job_db.db")
        session = sessionmaker(bind=engine)()
        
        session.add(db_job(job))
        session.commit()

def insert_company(company):

    engine = create_engine("sqlite:///job_db.db")
    session = sessionmaker(bind=engine)()
    session.add(db_company(company))
    session.commit()

def get_jobs():
    engine = create_engine("sqlite:///job_db.db")
    session = sessionmaker(bind=engine)()
    jobs = session.query(db_job).all()
    return jobs

def get_companies():
    engine = create_engine("sqlite:///job_db.db")
    session = sessionmaker(bind=engine)()
    companies = session.query(db_company).all()
    return companies


