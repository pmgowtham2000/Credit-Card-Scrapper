# Credit-Card-Scrapper
A scraping bot that can extract credit card information froma a PDF document.

I've created a script that extends your PDF extraction code to use the Gemini API for extracting credit card information. I have briefed it below:

It reads and extracts text from your PDF using PyPDF2 (keeping your original function)
It cleans up the extracted text to make it more suitable for API processing
It sends the text to the Gemini API to extract credit card details
It parses the response and saves the extracted information in JSON format

# How to use:

1. First, make sure you have the necessary packages installed from requirements.txt file

     pip install -r requirements.txt

3. Set up your Gemini API key as an environment variable in he "XX..XX" space provided in the code

4. Run the script with your PDF file path.

# Result

Extract all text from the PDF

Process the text with Gemini API to identify credit card details

Save the extracted data to a JSON file

Print a summary of the findings

The output JSON will contain all the credit card details you requested: card name, issuing bank, joining fee, annual fee, reward structure, and cashback offers.
