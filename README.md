# PDF Invoice Data Extraction
## Project Overview
This project involves extracting data from PDF invoices and converting it into CSV format. The extracted information includes fields like Total Amount, Date, PO Number, Invoice Number, Tax ID, Tax, Subtotal, and Shipping Charges. The project uses Python libraries such as pdf2image and pytesseract to convert PDFs to images and perform OCR (Optical Character Recognition).

## Files and Directories
- main.py: The main script to execute the extraction process.
- requirements.txt: A list of dependencies required for the project.
- input/: Directory where input PDF files should be placed.
- output/: Directory where the output CSV files will be saved.
## Setup Instructions
### Prerequisites
- Python 3.x
- Tesseract-OCR
### Install Tesseract-OCR
**Windows:** Download the installer from the [Tesseract GitHub repository](https://github.com/tesseract-ocr/tesseract) and follow the installation instructions.

### Install Python Dependencies
Create a virtual environment and install the dependencies listed in **requirements.txt**.
- pip install -r requirements.txt

## Usage
#### Prepare the input directory:
1. Place your PDF files in the **input/** directory.

2. Run the script:
Execute the main script to process the PDF files.
- python main.py

3. Check the output:
The extracted data will be saved as CSV files in the **output/** directory.
