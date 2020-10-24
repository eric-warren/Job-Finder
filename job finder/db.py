from sqlalchemy import create_engine , Column , Boolean, String, Integer, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from objects import job_c, company_c
from gen_parse import get_settings


def get_con_str():

    settings = get_settings()
    db_type = settings["db"]["db_type"]
    db_path = settings["db"]["path"]
    db_user = settings["db"]["username"]
    db_pass = settings["db"]["password"]

    if db_type == "sqlite":
        con_str = f"{db_type}:///{db_path}"
    else:
        con_str = f"{db_type}://{db_user}:{db_pass}@{db_path}"
    return con_str


def create_db():
    """
    This Functions is to create the DB and tables if it does not already exists
    """
    # Checks if the DB file job_db.db exsists and if it doesnt creates it

    if not database_exists(get_con_str()) and "sqlite" in get_con_str():
        create_database(get_con_str())

    # This is needed for SQL alchemy 
    engine = create_engine(get_con_str())

    # Creates the jobs table if it does not exists
    if not engine.dialect.has_table(engine, "jobs"):  
        metadata = MetaData(engine)
        # Create a table object with the appropriate Columns
        Table("jobs", metadata,
            Column('md5', String, primary_key=True), 
            Column('title', String), Column('isremote', Boolean), Column('company', String),
            Column('description', String), Column('city', String),
            Column('salary_low', Integer), Column('salary_high', Integer),
            Column('us_only', Boolean), Column('country', String),
            Column('country_code', String))
        # Implement the creation
        metadata.create_all()

    # Creates the companies table if it does not exists
    if not engine.dialect.has_table(engine, "companies"):
        metadata = MetaData(engine)
        # Create a table object with the appropriate Columns
        Table("companies", metadata,
            Column('name', String, primary_key=True))
        # Implement the creation
        metadata.create_all()

def get_session():
    """
    Gets a connection to DB

    Returns:
        SqlAlchemy session: used for connecting to DB
    """

    engine = create_engine(get_con_str())
    session = sessionmaker(bind=engine)()

    return session


def insert_job(job):
    """
    Inserts a new job into the Database

    Args:
        job (job_c): the job class found in objects.py
    """

    # Gets all the jobs from the DB
    all_jobs = get_jobs()


    # Checks to see if the MD5 hash exists and if it doesnt adds the job to the DB
    if not any(l_job.md5 == job.md5 for l_job in all_jobs):

        #Creates session with DB
        session = get_session()
        
        # Adds and commit to DB
        session.add(job)
        session.commit()
        session.expunge_all()
        session.close()
        return job
    else:
        return False


def insert_company(company):

    """
    Inserts a new company into the Database

    Args:
        company (company_c): the company class found in objects.py
    """

    # Gets all the companies form the DB
    all_companies = get_companies()

    # Checks to see if the company exists and if it doesnt adds the company to the DB
    if not any(comp.name == company.name for comp in all_companies):

        # Creates the session with the DB
        session = get_session()

        # Adds and commits to DB
        session.add(company)
        session.commit()
        session.expunge_all()
        session.close()

def get_jobs():
    """
    Gets all the Jobs from the DB

    Returns:
        list: The list is full of job_c objects
    """

    # Creates the session with the DB
    session = get_session()

    # Queries DB for all Jobs
    jobs = session.query(job_c).all()
    session.expunge_all()
    session.close()

    return jobs

def get_companies():
    """
    Gets all the Companies from the DB

    Returns:
        list: The list is full of company_c objects
    """

    # Creates the session with the DB
    session = get_session()

    # Queries DB for all Companies
    companies = session.query(company_c).all()
    session.expunge_all()
    session.close()

    return companies


create_db()