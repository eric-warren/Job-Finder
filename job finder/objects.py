class job_c:

    isremote = None
    company = None
    description = None
    city = None
    salary_low = None
    salary_high = None

    def __init__(self, title, url):
        self.title = title
        self.url = url


class company:

    def __init__(self, name,):
        self.name = name