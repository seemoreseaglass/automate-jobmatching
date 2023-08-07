# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import datetime
import os
import sqlite3
from itemadapter import ItemAdapter


class ScrapyJdGreenPipeline:
    _db = None

    @classmethod
    def get_database(cls):
        """
        Get the access to database and its table `job_desc` to store the scraped data if exists,
        if not create one.
        """
        cls._db = sqlite3.connect(
            os.path.join(os.getcwd(), 'scrapy_jd_green.db'))
        
        # Create a table
        cursor = cls._db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_desc(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                company_name TEXT NOT NULL,
                job_title TEXT NOT NULL,
                job_role TEXT NOT NULL,
                business_details TEXT NOT NULL,
                job_description TEXT NOT NULL,
                outline TEXT, 
                job_requirements TEXT NOT NULL,
                salary TEXT NOT NULL,
                job_location TEXT NOT NULL,
                job_benefits TEXT NOT NULL, 
            );
        """)

        return cls._db

    def process_item(self, item, spider):
        """
        This will be executed when the data is passed to Pipeline.
        Set `item` passed by `spider` as "item".
        """
        self.save_post(item)        

        return item

    def save_post(self, item):
        """
        Save `item` into the database.
        """
        if self.find_post(item['url']):
            # If the job description with the same url exists, skip the process
            return
        db = self.get_database()
        db.execute("INSERT INTO dob_desc (url, company_name, job_title, job_role, business_details, job_description, outline, job_requirements, salary, job_location, job_benefits) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
            item['url'],
            item['company_name'],
            item['job_title'],
            item['job_role'],
            item['business_details'],
            item['job_description'],
            item['outline'],
            item['job_requirements'],
            item['salary'],
            item['job_location'],
            item['job_benefits'],
        ))
        db.commit()

    def find_post(self, url):
        """
        Find a job description where is the url is `url`
        """
        db = self.get_database()
        cursor = db.execute(
            "SELECT * FROM job_desc WHERE url=?",
            (url,)
        )
        return cursor.fetchone()