import requests
from bs4 import BeautifulSoup
import csv





class WebNewsScraper():





    def scrape_detailed_dataset(self, dataset_url):
        response = requests.get(dataset_url)
        soup = BeautifulSoup(response.text, 'html.parser')



        #specific requirements that we're looking for in the site to be scraped
        dataset_name = soup.find('h1', class_='text-3xl font-semibold text-primary-content')#what we're trying to find
        dataset_name = dataset_name.text.strip() if dataset_name else "N/A" #conditional if found or not

        donated_date = soup.find('h2', class_='text-sm text-primary-content')
        donated_date = donated_date.text.strip().replace('Donated on ', '') if donated_date else "N/A"


        description = soup.find('p')
        description = description.text.strip() if description else "N/A" #just find any <p> element

        details = soup.find_all('div', class_='col-span-4')


        #ANALOGY OF THE CODE BELOW
        # so each div is a different box, and we're looking at 6 boxes, each box having a unique
        # data to be scraped... if those boxes are empty its N/A.
        # So details is the reference of the type of structured data we're trying to find
        # in each box, on details[0] we're expecting to find element <p> thats being structured
        # in a class='col-span-4'"

        #SAMPLE
        # <div class="col-span-4">
        #     <p>Time-Series</p>  #This is dataset_characteristics 
        # </div>
        # <div class="col-span-4">
        #     <p>Healthcare</p>  #This is subject_area 
        # </div>
        # <div class="col-span-4">
        #     <p>Classification</p>  #This is associated_tasks 
        # </div>

        dataset_characteristics = details[0].find('p').text.strip() if len(
            details) > 0 else "N/A"
        subject_area = details[1].find('p').text.strip() if len(
            details) > 1 else "N/A"
        associated_tasks = details[2].find('p').text.strip() if len(
            details) > 2 else "N/A"
        feature_type = details[3].find('p').text.strip() if len(
            details) > 3 else "N/A"
        instances = details[4].find('p').text.strip() if len(
            details) > 4 else "N/A"
        features = details[5].find('p').text.strip() if len(
            details) > 5 else "N/A"


        return [
                    dataset_name, donated_date, description, dataset_characteristics,
                    subject_area, associated_tasks, feature_type, instances, features
                ]
    def scrape_datasets(self, page_url, data, limit):
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')



        dataset_list = soup.find_all('a', class_='link-hover link text-xl font-semibold')

        if not dataset_list:
            print("No dataset links found")
            return
        
        for dataset in dataset_list:
            if len(data) >= limit:
                return 0
            dataset_link = "https://archive.ics.uci.edu" + dataset['href']
            print(f"Scraping details for {dataset.text.strip()}...")
            dataset_details = self.scrape_detailed_dataset(dataset_link)
            data.append(dataset_details)
    

    def scrape_sources(self, limit = 40): #fixed limit if the given limit fails
        # base_url = "https://archive.ics.uci.edu/datasets"#web homepage
        base_url = "https://feeds.bbci.co.uk/news/world/rss.xml"#web homepage



        headers = ["Dataset Name", "Donated Date", "Description",
                   "Dataset Characteristics", "Subject Area", "Associated Tasks",
                   "Feature Type", "Instances", "Features"] #csv headers what type of data will be scraped


        data = []
        skip = 0
        take = 10
        while len(data) < limit:
            page_url = f"https://archive.ics.uci.edu/datasets?skip={skip}&take={take}&sort=desc&orderBy=NumHits&search="
            print(f"Scraping page: {page_url}")
            initial_data_count = len(data)
            self.scrape_datasets(page_url, data, limit)
            if len(
                    data
            ) == initial_data_count: 
                break
            skip += take

        with open('uci_datasets.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)


        print("Scraping complete. Data saved to 'uci_datasets.csv'.")




scrape = WebNewsScraper()
print(scrape.scrape_sources(limit=30)) #overriding the fix limit






