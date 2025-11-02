import re
import json
from base_extractor import extract_text_pypdf2, extract_text_pdfplumber


def extract_hdfc_details(pdf2_text, plumber_text):
    """
    Extract structured details from an HDFC Bank credit card statement.
    Combines PyPDF2 and pdfplumber text for higher accuracy.
    """
    details = {
        "bank": "HDFC",
        "card_last4": None,
        "statement_date": None,
        "payment_due_date": None,
        "new_balance": None,
        "min_amount_due": None,
        "billing_cycle": None,
        "confidence": 0.0
    }

   
    #  Statement Date 
    
   
    #  Statement Date 
    
    statement_patterns = [
        r"Statement\s*Date\s*[:\-]?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",
        r"StatementDate\s*[:\-]?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",
        r"Statement\s*Dt\s*[:\-]?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",
    ]
    for pattern in statement_patterns:
        match = re.search(pattern, plumber_text, re.IGNORECASE)
        if match:
            details["statement_date"] = match.group(1)
            break

    #  Card Number 

    #  Card Number 

    card_patterns = [
        r"Card\s*No[: ]*\s*\d{4}\s*\d{2}XX\s*XXXX\s*(\d{4})",
        r"Card\s*Ending\s*Number\s*[:\-]?\s*(\d{4})",
        r"X{2,}\s?(\d{4})",
    ]
    for pattern in card_patterns:
        card_match = re.search(pattern, pdf2_text, re.IGNORECASE)
        if card_match:
            details["card_last4"] = card_match.group(1)
            break

      #  Payment Table
      #  Payment Table
    table_pattern = re.search(
        r"Payment\s*Due\s*Date\s+Total\s+Dues\s+Minimum\s+Amount\s+Due\s*\n?"
        r"\s*([0-9]{2}/[0-9]{2}/[0-9]{4})\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})",
        pdf2_text,
        re.IGNORECASE
    )
    if table_pattern:
        details["payment_due_date"] = table_pattern.group(1)
        details["new_balance"] = table_pattern.group(2).replace(",", "")
        details["min_amount_due"] = table_pattern.group(3).replace(",", "")


    #  Billing Cycle 

    #  Billing Cycle 
    billing_cycle_match = re.search(
        r"Billing\s*Cycle\s*[:\-]?\s*([0-9]{2}/[0-9]{2}/[0-9]{4})\s*-\s*([0-9]{2}/[0-9]{2}/[0-9]{4})",
        plumber_text,
        re.IGNORECASE
    )
    if billing_cycle_match:
        details["billing_cycle"] = f"{billing_cycle_match.group(1)} - {billing_cycle_match.group(2)}"

    
    #  Confidence Score
    
    #  Confidence Score
    filled = sum(1 for v in details.values() if v not in [None, "", 0.0])
    details["confidence"] = round(filled / len(details), 2)

    return details


def parse_hdfc_statement(file_path):
    """
    Wrapper to process HDFC PDF and return extracted JSON-like dict.
    """
    # Extract both versions of text
    pdf2_text = extract_text_pypdf2(file_path)
    plumber_text = extract_text_pdfplumber(file_path)

    # Extract structured fields
    data = extract_hdfc_details(pdf2_text, plumber_text)

    print("\n----  FINAL HDFC OUTPUT ----")
    print("\n----  FINAL HDFC OUTPUT ----")
    print(json.dumps(data, indent=2))
    return data


# -------------------------------
# 🔹 Run directly for testing
# -------------------------------
if __name__ == "__main__":
    file_path = r"examples\hdfc.pdf"  
    file_path = r"examples\hdfc.pdf"  
    parse_hdfc_statement(file_path)