# Copyright 2022 typicat
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# needs
from bs4 import BeautifulSoup
import requests
from rich.console import Console
from rich.table import Table

# set up scraping
url = f"https://kagealven.com/fangstrapporter-aktuella/"
header = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 Safari/537.36'
}
html = requests.get(url, headers=header)
if html.status_code != 200:
    html.raise_for_status()
soup = BeautifulSoup(html.content, "html.parser")

# create table for displaying results
table = Table(title="Fångstrapporter Kågeälven")

table.add_column("Datum", style="dim")
table.add_column("Namn")
table.add_column("Art", style="magenta bold")
table.add_column("Längd")
table.add_column("Sätt")
table.add_column("Plats", justify="right")

# algorithm displaying catches
lax = 0
oring = 0
data = soup.find('table').find_all('tr')
for row in data:
    td = row.find_all('td')
    namn = td[0].get_text()
    datum = td[1].get_text()
    art = td[2].get_text()
    if art=="Lax":
        lax+=1
    elif art=="Öring":
        oring+=1
    satt  = td[7].get_text()
    langd = td[8].get_text()
    plats = td[10].get_text()
    table.add_row(datum, namn, art, langd, satt, plats)

# wrap up and display nicely
console = Console()
console.print(table)
print(f"Lax: {lax} \t Öring: {oring}")
