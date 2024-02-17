import chardet
import requests
from bs4 import BeautifulSoup
import csv
API_KEY = 'AIzaSyBiX4NXtl_VIcoI9gx0v4SqtFBKlZrC4Wc'
SEARCH_ENGINE_ID = '110efe96dacef4043'  # Replace with your search engine ID
queries = [
    "Canoo industry size, growth rate, trends, key players",
    "Canoo main competitors, market share, products, pricing strategies, marketing efforts",
    "Canoo market trends, consumer behavior, technological advancements, competitive landscape",
    "Canoo financial performance, revenue, profit margins, return on investment, expense structure"
]

# Output CSV file
output_csv_file = 'sample2.csv'

structured_data = []

# Function to perform the search


def google_search(query):
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': query,
        'exactTerms': 'Canoo'  # Exacts term parameter to ensure relevance
    }
    response = requests.get(url, params=params)
    return response.json()


# Perform searches and collects data
for query in queries:
    search_results = google_search(query)
    for item in search_results.get('items', []):
        structured_data.append({
            'title': item['title'],
            'link': item['link'],
            'snippet': item['snippet']
        })

# Saving the structured data to CSV
with open(output_csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['title', 'link', 'snippet'])
    writer.writeheader()
    for data in structured_data:
        writer.writerow(data)

print(f"Data has been written to {output_csv_file}")

# Function to scrape the content from the URL


def scrape_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            paragraphs = soup.find_all('p')
            content = ' '.join([para.get_text() for para in paragraphs])
            return content
        else:
            print(f"Failed to retrieve content from {url}")
            return ""
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return ""


def update_csv_with_content(input_csv_file, output_csv_file):
    with open(input_csv_file, mode='r', newline='', encoding='utf-8') as infile, \
            open(output_csv_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['content']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            content = scrape_content(row['link'])
            row['content'] = content
            writer.writerow(row)


update_csv_with_content('sample2.csv', 'sample_with_content.csv')

print(f"Content has been added to {output_csv_file}")
