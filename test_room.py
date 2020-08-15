from bs4 import BeautifulSoup
import requests

URL = "https://www.worldometers.info/coronavirus/country/uk/"

parsed_html = requests.get(URL)
soup = BeautifulSoup(parsed_html, "html.parser")

scripts = soup.find_all('script')
script = scripts[21].text
print(script)