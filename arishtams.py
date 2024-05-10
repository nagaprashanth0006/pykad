from bs4 import BeautifulSoup as BS
from pprint import pprint
from tabulate import tabulate

html = open("C:\\Users\\nagap\\Downloads\\arishtams.htm", "r").read()
soup = BS(html, parser="lxml")
pprint(soup)
