import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.rappler.com"
response = requests.get(url)
html_content = response.text
soup = BeautifulSoup(html_content, "html.parser")
target_tag = "h3"





heading = soup.find_all(target_tag)
n=len(heading)
if n <= 1:
    print(f"No content of {target_tag} found")

else:
    for i in range(n):
        print(str.strip(heading[i].text))




