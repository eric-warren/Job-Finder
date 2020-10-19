from indeed import search_indeed
from gen_parse import get_settings
from db import insert_job
from db import create_db
from time import sleep
import time


def update_jobs():
    start_time = time.time()

    create_db()
    settings = get_settings()
    new_jobs = []
    for location in settings['areas']:
        print(location)
        print(time.time()-start_time)
        sleep(10)
        for term in settings['search_keys']:
            print(term)
            print(time.time()-start_time)
            sleep(10)
            job_indeed = search_indeed(term, location['city'], location['country_code'], location['country'])
            for job in job_indeed:
                new_job = job
                inserted_job = insert_job(job)
                if inserted_job:
                    new_jobs.append(new_job)


    return new_jobs


new_jobs = update_jobs()

print(len(new_jobs))