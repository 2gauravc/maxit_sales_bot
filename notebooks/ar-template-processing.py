import os
import json
from typing import Optional
from pdfminer.high_level import extract_text
from pydantic import BaseModel, Field
from datetime import date
from langchain.chat_models import init_chat_model

# --- Define the schema
class ARMetadataSchemaModel(BaseModel):
    company_name: str = Field(..., description="Name of the company")  # mandatory
    ticker: str = Field(..., description="Stock ticker symbol")  # mandatory
    exchange: str = Field(..., description="Stock exchange where listed, e.g. NASDAQ")  # mandatory
    reporting_period_ending_date: str = Field(..., description="Fiscal period ending date")  # mandatory
    report_language: Optional[str] = Field(None, description="Language of the report")
    

def extract_text_pdf(pdf_path: str, num_pages: int) -> bool:
    try:
        return extract_text(pdf_path, maxpages=num_pages).strip()
    except Exception:
        return ""
    

# --- Main runner
def main(pdf_path: str):
    num_pages = 2
    n_page_text = extract_text_pdf(pdf_path, num_pages)

    if not n_page_text:
        print("🚫 The file appears to be an image-based PDF or unreadable.")
        return
    
    llm = init_chat_model("gpt-4o-mini", model_provider="openai")

    structured_llm = llm.with_structured_output(ARMetadataSchemaModel)
    res = structured_llm.invoke(n_page_text)
    print(res)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python extract_ar_data.py path/to/annual_report.pdf")
        exit(1)

    main(sys.argv[1])
