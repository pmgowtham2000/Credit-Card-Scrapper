from PyPDF2 import PdfReader
import json
import os
import re
from google.generativeai import configure, GenerativeModel
import google.generativeai as genai

os.environ["GEMINI_API_KEY"]="XXXXXXXXXXXXXXXXXXXXXX"

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def clean_pdf_text(text):
    text = re.sub(r'\s+', ' ', text) # In order to remove non-printable characters
    text = re.sub(r'[^\x20-\x7E\n]', '', text)  # For limiting text length 
    max_length = 30000 
    if len(text) > max_length:
        text = text[:max_length]
    return text

def extract_credit_cards_with_gemini(pdf_text):
    """Extract credit card information using Gemini API."""
    # Configure the Gemini API with your API key
    api_key = os.environ.get("GEMINI_API_KEY")
    configure(api_key="XXXXXXXXXXXXXXXXXXXXXXXXXXX")
    
    # Create a model instance
    model = GenerativeModel('gemini-1.5-pro')
    
    # Clean the text
    clean_text = clean_pdf_text(pdf_text)
    
    # Prepare the prompt
    prompt = f"""
    Extract all credit card information from the following text. Return ONLY a JSON array where each item is a credit card with the following fields:
    - card_name: The name of the credit card
    - issuing_bank: The bank that issues the card (if available)
    - joining_fee: The fee to join or apply for the card
    - annual_fee: The yearly fee for the card
    - reward_structure: Details about reward points or benefits
    - cashback_offers: Information about cashback or offers
    
    Only include fields where information is available. If a field is not mentioned, omit it from the JSON.
    
    Here is the text to analyze:
    
    {clean_text}
    """
    
    # Call the Gemini API
    response = model.generate_content(prompt)
    
    # Extract and parse the JSON response
    json_text = extract_json_from_response(response.text)
    
    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from API response: {e}")
        print(f"Raw response: {json_text}")
        return []

def extract_json_from_response(response_text):
    """Extract JSON content from the API response text."""
    # Look for JSON array in the response
    json_match = re.search(r'\[\s*{.+}\s*\]', response_text, re.DOTALL)
    if json_match:
        return json_match.group(0)
    
    # If no array is found, look for a single JSON object
    json_match = re.search(r'{.+}', response_text, re.DOTALL)
    if json_match:
        return f"[{json_match.group(0)}]"
    
    # If no JSON is found, return an empty array
    return "[]"

def save_to_json(data, output_path):
    """Save the extracted data to a JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Saved data to {output_path}")

if __name__ == "__main__":
    
    pdf_file = r"C:\Users\pmgow\Downloads\sosc-credit-cards.pdf"
    output_file = "extracted_credit_cards.json"
    
    print(f"Extracting text from {pdf_file}...")
    pdf_text = extract_text_from_pdf(pdf_file)
    print(f"Extracted {len(pdf_text)} characters from PDF")
    
    if pdf_text:
        print("Sample text from PDF (first 200 characters):")
        print(pdf_text[:200])
        print("\nExtracting credit card information using Gemini API...")
        
        credit_cards = extract_credit_cards_with_gemini(pdf_text)
        
        print(f"Extracted {len(credit_cards)} credit cards")
        if credit_cards:
            save_to_json(credit_cards, output_file)
            for i, card in enumerate(credit_cards):
                print(f"\nCard {i+1}: {card.get('card_name', 'Unknown')}")
                print(f"  Bank: {card.get('issuing_bank', 'Not specified')}")
                print(f"  Joining Fee: {card.get('joining_fee', 'Not specified')}")
                print(f"  Annual Fee: {card.get('annual_fee', 'Not specified')}")
    else:
        print("No text was extracted from the PDF")
