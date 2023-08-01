import scrapy
from scrapy.http import FormRequest
from scrapy_jd_green.items import JobDescription
import json

# Read the configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)
email = config["email"]
password = config["password"]
print(email)
print(password)

class ScrapyJdGreenSpiderSpider(scrapy.Spider):
    name = "scrapy_jd_green_spider"

    def start_requests(self):
        """
        Start requests with login info
        """
        login_url = "https://www.green-japan.com/login"
        # Start the login page request
        return [scrapy.Request(login_url, callback=self.login)]

    def login(self, response):
        """
        Handle login
        """
        # Fetch the authenticity token
        authenticity_token = response.css("input[name='authenticity_token']::attr(value)").get()
        print(authenticity_token)
        # Create a form data dictionary with the required information
        formdata = {
            'utf8': '✓',
            'authenticity_token': authenticity_token,
            'target_url': 'https://www.green-japan.com/',
            'user[mail]': email,
            'user[password]': password,
            'commit': 'ログイン'
        }
        # Submit a POST request to the login page
        return FormRequest.from_response(response, formdata=formdata, callback=self.start_scraping)

    def start_scraping(self, response):
        """
        Start scraping
        This function is called when the login is successful.
        """
        # Check login succeed before proceeding
        if response.status == 302:
            self.logger.info("Successfully logged in.")
            # Start scrawling
            yield scrapy.Request("https://www.green-japan.com/search_key?key=xmy3i3jpu05ojorlyysq&keyword=AI%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2", callback=self.parse_results)

        else:
            self.logger.error("Login failed.")
            return

    def parse_results(self, response):
        """
        Parse the search results page
        """
        # Get the job description links
        for item_link in response.css(".job-card__job-link a::attr(href)").get():
            yield scrapy.request(response.urljoin(item_link), callback=self.parse_item)


    def parse_item(self, response):
        """
        Parse the job description page
        """
        url = response.url
        job_title = response.css('.css-1bp4cqx::text').get()
        print(job_title)
        job_role = response.css('.css-1fcpmhi::text')[0].get()
        print(job_role)
        business_details = response.css('.css-sr5sh7::text')[0].get()
        print(business_details)
        job_description = response.css('.css-sr5sh7::text')[1].get()
        print(job_description)
        outline = response.css('.css-abo7h2::text')[1].get()
        print(outline)
        job_requirements = response.css('.css-abo7h2::text')[2].get()
        print(job_requirements)
        salary = response.css('.css-abo7h2::text')[4].get()
        print(salary)
        selection_process = response.css('.css-abo7h2::text')[6].get()
        print(selection_process)
        job_location = response.css('.css-abo7h2::text')[7].get()
        print(job_location)
        job_benefits = response.css('.css-abo7h2::text')[9].get()
        print(job_benefits)

