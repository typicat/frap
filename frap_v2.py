#!/usr/bin/env python3
"""
Copyright 2022 Karl Jonsson 

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table

header = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 Safari/537.36",
}


def scrape():
    url = "https://kagealven.com/fangstrapporter-aktuella/"
    html = requests.get(url, headers=header)
    if html.status_code != 200:
        html.raise_for_status()
    soup = BeautifulSoup(html.content, "lxml")
    res = soup.find("table").find_all("tr")
    return res

def draw_table() -> None:
    lax = oring = spinn = fluga = 0
    table = Table(title="Fångstrapporter Kågeälven")
    table.add_column("Datum", style="dim")
    table.add_column("Namn")
    table.add_column("Art", style="green")
    table.add_column("Längd (cm)")
    table.add_column("Metod")
    table.add_column("Plats")
    s_table = Table(title="Statistik 2022")
    s_table.add_column("Öring")
    s_table.add_column("Lax")
    s_table.add_column("Spinn")
    s_table.add_column("Fluga")

    data = scrape()
    for row in data:
        td = row.find_all("td")
        namn = td[0].get_text()
        datum = td[1].get_text()
        art = td[2].get_text()
        if art == "Lax":
            lax += 1
        elif art == "Öring":
            oring += 1
        metod = td[7].get_text()
        if metod == "Spinn":
            spinn += 1
        elif metod == "Fluga":
            fluga += 1
        langd = td[8].get_text() + " cm"
        plats = td[10].get_text()
        table.add_row(datum, namn, art, langd, metod, plats)
    console = Console()
    console.print(table)
    s_table.add_row(str(oring), str(lax), str(spinn), str(fluga))
    console.print(s_table)

def main() -> None:
    draw_table()

if __name__ == "__main__":
    main()
