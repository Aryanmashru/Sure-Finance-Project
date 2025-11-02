import re
import json
import pdfplumber
from base_extractor import extract_text_pypdf2, extract_text_pdfplumber


def extract_idfc_details(pdf2_text, plumber_text, file_path):
    details = {
        "bank": "IDFC",
        "card_last4": None,
        "statement_date": None,
        "payment_due_date": None,
        "new_balance": None,
        "min_amount_due": None,
        "billing_cycle": None,
        "confidence": 0.0
    }

    #  Extract 2x2 table data
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if not table:
                    continue

                # Flatten and clean text from table
                flat = [" ".join([cell.strip() if cell else "" for cell in row]) for row in table]
                combined = " ".join(flat)

                # Detect main fields
                if (
                    "Statement Date" in combined
                    and "Payment Due Date" in combined
                    and "Total Amount Due" in combined
                    and "Minimum Amount Due" in combined
                ):
                    # Extract Dates
                    dates = re.findall(r"(\d{2}/\d{2}/\d{4})", combined)
                    if len(dates) >= 2:
                        details["statement_date"] = dates[0]
                        details["payment_due_date"] = dates[1]

                    # Extract Amounts
                    amts = re.findall(r"r?\s*([\d,]+\.\d{2})", combined)
                    if len(amts) >= 2:
                        details["new_balance"] = amts[0].replace(",", "")
                        details["min_amount_due"] = amts[1].replace(",", "")

    #  Extract Card Number 
    card_match = re.search(
        r"Card\s*Number\s*[:\-]?\s*(?:\d{4}[\s*Xx*]*){2,3}(\d{4})", plumber_text, re.IGNORECASE
    )
    if not card_match:
        card_match = re.search(r"(\d{4})\s*[\*Xx]{2,}\s*(\d{4})", plumber_text)
        if card_match:
            details["card_last4"] = card_match.group(2)
    else:
        details["card_last4"] = card_match.group(1)

    #  Confidence score
    filled = sum(1 for v in details.values() if v not in [None, ""])
    details["confidence"] = round(filled / len(details), 2)

    return details


def parse_idfc_statement(file_path):
    pdf2_text = extract_text_pypdf2(file_path)
    plumber_text = extract_text_pdfplumber(file_path)

    data = extract_idfc_details(pdf2_text, plumber_text, file_path)

    print("\nDetected: IDFC Bank Statement ✅")
    print(json.dumps(data, indent=2))
    return data


# ---------- Run ----------
if __name__ == "__main__":
    file_path = r"examples\idfc-2.pdf"
    parse_idfc_statement(file_path)
