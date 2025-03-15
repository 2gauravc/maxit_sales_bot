import requests

# Set SEC Headers
headers = {
    "User-Agent": "Your Name (your-email@example.com)"
}

# Step 1: Get CIK for a Company
ticker = "AAPL"
cik_lookup_url = "https://www.sec.gov/files/company_tickers.json"
response = requests.get(cik_lookup_url, headers=headers).json()
cik = next((str(c["cik_str"]).zfill(10) for c in response.values() if c["ticker"] == ticker), None)

if cik:
    print(f"CIK for {ticker}: {cik}")

    # Step 2: Get Latest 10-K Filing
    filings_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    filings = requests.get(filings_url, headers=headers).json()

    ten_k_filings = [
        filings["filings"]["recent"]["accessionNumber"][i]
        for i, form in enumerate(filings["filings"]["recent"]["form"])
        if form == "10-K"
    ]

    if ten_k_filings:
        accession_number = ten_k_filings[0]
        print(f"Latest 10-K Accession Number: {accession_number}")

        # Step 3: Construct the Filing URL and Find PDF
        accession_formatted = accession_number.replace("-", "")
        filing_base_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession_formatted}/"
        filing_index_url = filing_base_url + "index.html"

        print(f"Filing URL: {filing_index_url}")

        # Download Filing Page and Search for PDFs
        filing_page = requests.get(filing_index_url, headers=headers).text
        pdf_links = [line.split('"')[1] for line in filing_page.split() if ".pdf" in line.lower()]

        if pdf_links:
            pdf_url = "https://www.sec.gov" + pdf_links[0]
            print(f"Downloading PDF: {pdf_url}")

            pdf_response = requests.get(pdf_url, headers=headers)
            with open(f"{ticker}_10K.pdf", "wb") as f:
                f.write(pdf_response.content)

            print("PDF Downloaded Successfully!")
        else:
            print("No PDF found in the filing.")

    else:
        print("No 10-K filings found.")
else:
    print("CIK not found.")
