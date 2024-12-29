# CraftyCult Product Crawler

This repository contains a Python script designed to crawl product pages from `https://craftycult.com/product/` and extract structured information in Markdown format. The extracted data is AI-friendly and ready for use in machine learning tasks or documentation.

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

---
