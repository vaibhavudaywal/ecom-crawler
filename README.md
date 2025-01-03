# Ecom Product Crawler

This repository contains a Python script designed to crawl product pages from `https://craftycult.com/product/`(Any Ecom store url where you could extract product's data) and extract structured information in Markdown format. The extracted data is AI-friendly and ready for use in machine learning tasks or documentation.

---

## Features

- **Targeted Crawling**:
  - Focuses only on product pages matching the pattern `https://craftycult.com/product/`.

- **Structured Markdown Output**:
  - Extracted product data includes:
    - Title
    - URL
    - Description
    - Specifications (if available)

- **Server-Friendly**:
  - Includes a delay between requests to avoid overloading the website.

---

## Output Format

The script generates a `product_data.md` file with the following structure:

```markdown
# Extracted Product Data

## Example Product Title

**URL**: [https://craftycult.com/product/example-product](https://craftycult.com/product/example-product)

**Description**:

This is a sample product description.

**Specifications**:

- Feature 1
- Feature 2
- Feature 3

```
---

## In action

- **Crawling the ecom store product pages**
<img width="726" alt="image" src="https://github.com/user-attachments/assets/3b7ac047-9f81-45be-9656-a47aab617f07" />

- **Extracted the meaningful data from product page in markdown format**
<img width="1168" alt="image" src="https://github.com/user-attachments/assets/f95f229f-0f5c-41ad-987e-b654bbb346e7" />

- **ChatBot (backend) in action**
<img width="829" alt="image" src="https://github.com/user-attachments/assets/444c0f7d-215e-4cc9-89ce-8bb071fb1e75" />

- **Integrated on store**
<img width="1098" alt="image" src="https://github.com/user-attachments/assets/fb63b627-5d7f-45cd-b78a-9c36f5f54988" />

---

