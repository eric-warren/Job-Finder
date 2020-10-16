from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import MetaData

if not database_exists("sqlite:///job_db.db"):
    create_database("sqlite:///job_db.db")
engine = create_engine("sqlite:///job_db.db")

session = sessionmaker(bind=engine)()

base = declarative_base()


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


from objects import job_c
from objects import company_c

job = job_c("title",company_c("company"), "https://")
job.description = "Windows System & Network Administrator - Ottawa, ON (with regular travel to Kingston ON)About IOSiInternal Office Solutions Inc. (IOSi) was founded in 1998 and was formed as a private joint-stock company in February 2001 in Ottawa, Ontario Canada. IOSi holds a leading position in the Canadian market for systems integration. We are a small business with seven employees located in Ottawa on Auriga Driven and operate from several home offices where we provide remote as well as on site support services for our clients. IOSi is looking for a resource based in Ottawa ON, to manage public clouds and private virtual networks.IOSi is highly successful and competitive within the MSP marketplace due to its project implementation, utilization of the most reliable equipment and software produced by leaders of the North American computer market, as well as the professionalism of its staff.RESPONSIBILITIES The IT Support Administrator is responsible for performing the following duties;1. On site client support 60-70% (vehicle required)Provide on-site technical services to clients,Respond to escalation requests from our Office Coordinator,Respond to emergency requirements in a timely and efficient manner, andProvide issue resolution documentation to clients who opened the support ticket.2. Network DeploymentInterface with team members as it pertains to the deployment strategy,Team lead the deployment on-site, andManage the work of the 3rd party/partners assigned to the deployment.TECHNICAL REQUIREMENTSThe IT Support Administrator must have a good working knowledge of Windows 2008/2012/2016, Windows 7/10 Professional, and MS Office 365. Knowledge of Networking, Server, and Vmware/UNIX is required.The candidate must have a minimum of two years working knowledge of Microsoft networks, operating systems, MS Office Suites and obtained a College Diploma or equivalent in Information Technology. Vmware, Web application hosting experience and/or network security experience is desirable. The engineer must demonstrate an aptitude for technical products that will enable him/her to quickly understand IOSi's security solution set as well as broaden their client-server expertise. Knowledge of SolarWinds N-Central, Connectwise Manage, Microsoft O365, WatchGuard Firewalls, Lenovo, IBM, HP and Cisco products will also be of great benefit to the potential candidate for this position.Working closely with other team members, the IT Support Administrator is responsible for the technical aspects of client support and installation of products. Current Microsoft certification desirable.PERSONAL SKILLSThe IT Support Administrator must present a professional appearance and demeanor, possess strong interpersonal skills, strong telephone skills and etiquette and be able to relate to a small team of technical staff and managers. The candidate will need strong verbal and written communication skills to effectively participate in the sales cycle and to prepare deliverables. A driver�s license and vehicle is required for this position.Bilingual candidates are preferred.Starting Salary: $50,000.00 � $65,000.00 per yearJob Type: Full-timeSalary: $50,000.00-$65,000.00 per yearCOVID-19 considerations:Employees stay safe by working remotely. When onsite client support or in person interaction is required, masks & hand sanitizer are provided to employees.Experience:SolarWinds N-Central: 1 year (Preferred)IT system administration: 2 years (Required)Connectwise Manage: 1 year (Preferred)Firewall and Security: 2 years (Required)Microsoft O365: 1 year (Preferred)Work remotely:Yes"
company = company_c("my_company")


#session.add(db_company(company))
#session.commit()

session.add(db_job(job))
session.commit()