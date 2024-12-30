import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

# Constants for configuration
BASE_URL = "https://example.com/"  # Change this to your desired e-commerce domain
PRODUCT_URL_PATTERN = "/product/"  # Pattern to identify product URLs
TITLE_CLASSES = ["product-title", "et_pb_wc_title"]  # List of possible classes for product titles
DESCRIPTION_CLASSES = ["product-description", "et_pb_wc_description"]  # List of possible classes for descriptions
DETAILS_TAGS = {"p": {"style": "text-align: center;"}}  # Tags and attributes to locate product details

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
        title_text = "No Title"
        for title_class in TITLE_CLASSES:
            title = soup.find(class_=title_class)
            if title:
                title_text = title.get_text(strip=True)
                break

        # Extracting product description
        description_text = "No Description Available"
        for description_class in DESCRIPTION_CLASSES:
            description = soup.find(class_=description_class)
            if description:
                description_text = description.get_text(strip=True)
                break

        # Extracting product details
        product_details = []
        for tag, attrs in DETAILS_TAGS.items():
            details_section = soup.find_all(tag, attrs=attrs)
            for detail in details_section:
                detail_text = detail.get_text(strip=True)
                if detail_text:
                    product_details.append(detail_text)
        if not product_details:
            product_details.append("No product details found.")

        # Appending data in Markdown format
        markdown_content += f"## {title_text}\n\n"
        markdown_content += f"**URL**: [{url}]({url})\n\n"
        markdown_content += f"**Description**:\n\n{description_text}\n\n"
        markdown_content += f"**Product Details**:\n\n"
        markdown_content += "\n".join(product_details) + "\n\n"
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
                        PRODUCT_URL_PATTERN in full_url and
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
    crawl_website(BASE_URL)

    # Save Markdown content to a file
    with open("product_data.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print("Data extraction completed. Markdown saved as 'product_data.md'.")

if __name__ == "__main__":
    main()
