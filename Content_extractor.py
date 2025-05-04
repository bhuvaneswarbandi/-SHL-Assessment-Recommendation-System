import requests
from bs4 import BeautifulSoup
import json
import time

with open('test_links.json','r') as json_links_file:
    links_data = json.load(json_links_file)

final_contents = []

for obj in links_data:
    title=obj["text"]
    link=obj['url']
    remote_testing=obj['remote_testing']
    adaptive_irt=obj['adaptive_irt']
    # print(link)
    try:
        url = f'https://www.shl.com{link}'
        response = requests.get(url,timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        content_divs = soup.find_all(class_='product-catalogue-training-calendar__row')
        page={}
        page['url']=url
        page['title']=title
        page['remote_testing']=remote_testing
        page['adaptive_irt']=adaptive_irt
        
        for div in content_divs:
            header = div.find(['h1', 'h2', 'h3','h4'])
            paragraph = div.find('p')
            # print(header)
            # print(paragraph)

            extracted_title = header.get_text(strip=True) if header else "No Title"
            content = paragraph.get_text(strip=True) if paragraph else "No Content"
            page[extracted_title]=content

        final_contents.append(page)
        
    except Exception as e:
            print(f"Error fetching {url}: {e}")
            continue

    
# Save final data
with open('structured_content_data.json', 'w',encoding='utf-8') as f:
    json.dump(final_contents, f, indent=4,ensure_ascii=False)

print("Data extracted and saved to content_data.json")
