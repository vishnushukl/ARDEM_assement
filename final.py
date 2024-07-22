import os
import re
import pandas as pd
from pdf2image import convert_from_path
import pytesseract

def extractedTxt(file):
    keywords = {
        'total amount': ['total amount', 'total', 'amount'],
        'date': ['date'],
        'po number': ['po number', 'purchase order', 'po'],
        'invoice number': ['invoice number', 'invoice'],
        'tax id': ['tax id', 'tax identification'],
        'tax': ['tax', 'sales tax'],
        'subtotal': ['subtotal'],
        'shipping charges': ['shipping charges', 'shipping']
    }
    
    extracted_data = {key: "No data found" for key in keywords}
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    
    try:
        if file.endswith(".pdf"):
            images = convert_from_path(file)
            for img in images:
                custom_config = r'--oem 3 --psm 6'  # OCR Engine Mode 3 and Page Segmentation Mode 6
                text = pytesseract.image_to_string(img, config=custom_config).lower().splitlines()
                
                joined_text = ' '.join(text)
                date_match = re.search(date_pattern, joined_text)
                extracted_date = date_match.group() if date_match else "No data found"
                
                for line in text:
                    for key, variations in keywords.items():
                        for variation in variations:
                            if key == "date":
                                extracted_data[key] = extracted_date
                            elif variation in line:
                                value = line.split(variation)[-1].strip().strip('|').strip('#:')
                                extracted_data[key] = value
                                break
    except Exception as e:
        print(f"An error occurred while reading {file}: {e}")
        return None
    
    capitalized_data = {key.title(): value for key, value in extracted_data.items()}
    
    return capitalized_data

def extract_confidence(file):
    keywords = {
        'total amount': ['total amount', 'total', 'amount'],
        'date': ['date'],
        'po number': ['po number', 'purchase order', 'po'],
        'invoice number': ['invoice number', 'invoice'],
        'tax id': ['tax id', 'tax identification'],
        'tax': ['tax', 'sales tax'],
        'subtotal': ['subtotal'],
        'shipping charges': ['shipping charges', 'shipping']
    }
    
    confidence_data = {key: None for key in keywords}
    
    try:
        if file.endswith(".pdf"):
            images = convert_from_path(file)
            for img in images:
                data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
                for i, word in enumerate(data['text']):
                    for key, variations in keywords.items():
                        for variation in variations:
                            if variation in word.lower():
                                confidence = data['conf'][i]
                                confidence_data[key] = confidence
                                break
    except Exception as e:
        print(f"An error occurred while reading {file}: {e}")
        return None
    
    confidence_data = {key.title(): value for key, value in confidence_data.items()}
    
    return confidence_data

def create_dataframe(file):
    data = extractedTxt(file)
    confidence = extract_confidence(file)
    
    if data is None or confidence is None:
        return None
    
    rows = []
    for key in data.keys():
        rows.append({'Field': key, 'Data': data[key], 'Confidence Level': confidence[key]})
    
    df = pd.DataFrame(rows, columns=['Field', 'Data', 'Confidence Level'])
    
    return df

def process_pdfs(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            file_path = os.path.join(input_dir, filename)
            df = create_dataframe(file_path)
            if df is not None:
                csv_filename = os.path.splitext(filename)[0] + ".csv"
                csv_path = os.path.join(output_dir, csv_filename)
                df.to_csv(csv_path, index=False)
                print(f"Processed {filename} and saved to {csv_path}")

def main():
    input_dir = input("Enter the input directory path where PDF files are stored: ")
    output_dir = input("Enter the output directory path where CSV files will be stored: ")
    
    process_pdfs(input_dir, output_dir)

if __name__ == "__main__":
    main()
