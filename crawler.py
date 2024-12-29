"""
Repository: craftycult-product-crawler
This script is designed to crawl and extract structured product information from URLs starting with 
'https://craftycult.com/product/'. The data is saved in Markdown format, suitable for AI training or documentation.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

# List of visited URLs to avoid duplicates
visited_urls = set()

# String to store Markdown content
markdown_content = "# Extracted Product Data\n\n"

# Function to extract clean data from a webpage
def extract_data_from_page(url):
    """
    Extracts product title, description, and specifications from the given URL and formats it into Markdown.
    
    Args:
        url (str): The URL of the product page to extract data from.
    """
    global markdown_content
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting product title
        title = soup.find('h1', class_='product-title')
        title_text = title.get_text(strip=True) if title else "No Title"

        # Extracting product description
        description = soup.find('div', class_='product-description')
        description_text = description.get_text(strip=True) if description else "No Description Available"

        # Extracting product specifications or features
        specs = soup.find('ul', class_='product-specifications')
        specifications = (
            "\n".join(f"- {item.get_text(strip=True)}" for item in specs.find_all('li'))
            if specs
            else "No Specifications Provided"
        )

        # Appending data in Markdown format
        markdown_content += f"## {title_text}\n\n"
        markdown_content += f"**URL**: [{url}]({url})\n\n"
        markdown_content += f"**Description**:\n\n{description_text}\n\n"
        markdown_content += f"**Specifications**:\n\n{specifications}\n\n"
        markdown_content += "---\n\n"

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")

# Function to crawl the website starting from the base URL
def crawl_website(base_url):
    """
    Crawls the website and extracts data from product pages.
    
    Args:
        base_url (str): The starting URL for crawling.
    """
    to_visit = [base_url]

    while to_visit:
        current_url = to_visit.pop(0)
        if current_url not in visited_urls:
            visited_urls.add(current_url)
            print(f"Crawling {current_url}...")

            # Extract data from the current page
            extract_data_from_page(current_url)

            # Find all internal links on the page and add them to the queue
            try:
                response = requests.get(current_url)
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(current_url, href)

                    # Add only URLs matching the product pattern
                    if (urlparse(full_url).netloc == urlparse(base_url).netloc and
                        full_url.startswith("https://craftycult.com/product/") and
                        full_url not in visited_urls):
                        to_visit.append(full_url)
            except requests.exceptions.RequestException as e:
                print(f"Error crawling {current_url}: {e}")

            # Avoid overloading the server
            time.sleep(1)

# Main function to crawl and output the Markdown content
def main():
    """
    Entry point of the script. Initiates crawling and saves the output as a Markdown file.
    """
    base_url = "https://craftycult.com/product/"  # Starting URL pattern
    crawl_website(base_url)

    # Save Markdown content to a file
    with open("product_data.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print("Data extraction completed. Markdown saved as 'product_data.md'.")

if __name__ == "__main__":
    main()
