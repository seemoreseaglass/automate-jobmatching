import scrapy
from scrapy.http import FormRequest
from scrapy_jd_green.items import JobDescription
import json
from urllib.parse import urljoin

# Read the configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)
    email = config["email"]
    password = config["password"]

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
        if response.status == 200:
            self.logger.info("Successfully logged in.")
            # Start scrawling
            yield scrapy.Request("https://www.green-japan.com/api/v2/user/job_offers?area_ids%5B%5D=13&company_name_only_flg=false&keyword=AI%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2&new_flg=false&offset=0&order_type=job_offer_score&salary_bottom_id=&width_size=400", callback=self.parse_results)

        else:
            self.logger.error("Login failed.")
            return

    def parse_results(self, response):
        """
        Parse the search results page
        """
        # Get the job offer list
        for offer in json.loads(response.body)["job_offers"]:
            
            offer_id = offer["job_offer_id"]
            client_id = offer["client_id"]
            url = "/".join(["https://www.green-japan.com/company", str(client_id), "job", str(offer_id)])

            yield scrapy.Request(url, callback=self.parse_item)


    def parse_item(self, response):
        """
        Parse the job description page
        """

        yield JobDescription(
            url = response.url,
            company_name = response.xpath('//h6[contains(@class, "css-fw3r0w")]/text()').get(),
            job_title = response.xpath('//h1[contains(@class, "css-1bp4cqx")]/text()').get(),
            job_role = response.xpath('//span[contains(@class, "css-9iedg7")]/text()').get(),
            business_details = response.xpath('//h5[contains(@class, "css-sr5sh7") and contains(text(), "事業内容")]/following-sibling::p[contains(@class, "css-bw2zqj")]/text()').get(),
            job_description = response.xpath('//h5[contains(@class, "css-sr5sh7") and contains(text(), "仕事内容")]/following-sibling::p[contains(@class, "css-bw2zqj")]/text()').get(),
            outline = response.xpath('//p[text()="概要"]/following-sibling::p[contains(@class, "css-abo7h2")]/text()').get(),
            job_requirements = response.xpath('//p[text()="概要"]/following-sibling::p[contains(@class, "css-abo7h2")]/text()').get(),
            salary = response.xpath('//span[contains(text(), "万円") and contains(@class, "css-9iedg")]/text()').get(),
            job_location = response.xpath('//p[text()="勤務地"]/following-sibling::p[contains(@class, "css-abo7h2")]/text()').get(),
            job_benefits = response.xpath('//p[text()="待遇・福利厚生"]/following-sibling::p[contains(@class, "css-abo7h2")]/text()').get(),
        )