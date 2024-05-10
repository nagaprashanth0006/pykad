from bs4 import BeautifulSoup as BS
from requests import get
from pprint import pprint

# url = "https://learn.microsoft.com/en-us/credentials/certifications/azure-data-engineer/?practice-assessment-type=certification"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
#     "Accept": "*/*",
# }
# html = get(url, headers=headers).text
html = open("C:\\Users\\nagap\\Downloads\\de.htm").read()
soup = BS(html, parser="html")
links = soup.find_all("a", attrs={"class": "justify-self-stretch stretched-link"})

print("\n".join([x["href"] for x in links]))
