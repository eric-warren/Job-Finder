from sqlalchemy import create_engine , Column , Boolean, String, Integer, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from .objects import job_c, company_c

# This Functions is to create the DB and tables if it does not already exists
def create_db():
    # Checks if the DB file job_db.db exsists and if it doesnt creates it
    if not database_exists("sqlite:///job_db.db"):
        create_database("sqlite:///job_db.db")

    # This is needed for SQL alchemy 
    engine = create_engine("sqlite:///job_db.db")

    # Creates the jobs table if it does not exists
    if not engine.dialect.has_table(engine, "jobs"):  
        metadata = MetaData(engine)
        # Create a table object with the appropriate Columns
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
        # Create a table object with the appropriate Columns
        Table("companies", metadata,
            Column('name', String, primary_key=True))
        # Implement the creation
        metadata.create_all()


def insert_job(job):
    all_jobs = get_jobs()

    if job not in all_jobs:

        engine = create_engine("sqlite:///job_db.db")
        session = sessionmaker(bind=engine)()
        
        session.add(job)
        session.commit()

def insert_company(company):

    engine = create_engine("sqlite:///job_db.db")
    session = sessionmaker(bind=engine)()
    session.add(company))
    session.commit()

def get_jobs():
    engine = create_engine("sqlite:///job_db.db")
    session = sessionmaker(bind=engine)()
    jobs = session.query(job_c).all()
    return jobs

def get_companies():
    engine = create_engine("sqlite:///job_db.db")
    session = sessionmaker(bind=engine)()
    companies = session.query(company_c).all()
    return companies


