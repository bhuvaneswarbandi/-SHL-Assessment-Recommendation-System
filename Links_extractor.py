import requests
from bs4 import BeautifulSoup
import json

        #type:pages
types = {1: 32, 2: 12}
links = []

for typ, pages in types.items():
    for window in range(12, (pages * 12) + 1, 12):
        url = f'https://www.shl.com/products/product-catalog/?start={window}&type={typ}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if table:
            for row in table.find_all('tr'):
                columns = row.find_all('td')
    
                if len(columns) >= 3:
                 
                    a_tag = columns[0].find('a', href=True)
                    if a_tag:
                        text = a_tag.text.strip()
                        link = a_tag['href']

                        
                        remote_testing = 'Yes' if columns[1].find('span', class_='catalogue__circle -yes') else 'No'
                        adaptive_irt = 'Yes' if columns[2].find('span', class_='catalogue__circle -yes') else 'No'
                        

                        links.append({
                            'text': text,
                            'url': link,
                            'remote_testing': remote_testing,
                            'adaptive_irt': adaptive_irt
                        })


with open('test_links.json', 'w') as json_file:
    json.dump(links, json_file, indent=4)

print("Links with features extracted and saved to test_links.json")
