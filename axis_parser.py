import re
import json
from base_extractor import extract_text_pypdf2, extract_text_pdfplumber


def extract_axis_details(pdf2_text, plumber_text):
    details = {
        "bank": "AXIS",
        "card_last4": None,
        "statement_date": None,
        "payment_due_date": None,
        "new_balance": None,
        "min_amount_due": None,
        "billing_cycle": None,
        "confidence": 0.0
    }

    #  Card Number
    card_match = re.search(r"Card\s*No[: ]*\s*\d{4,6}\*+\d{4}", pdf2_text, re.IGNORECASE)
    if card_match:
        digits = re.sub(r"\D", "", card_match.group())
        details["card_last4"] = digits[-4:]
        print(f"✅ Card ending: {details['card_last4']}")

    #  Payment summary table
    table_match = re.search(
        r"Total\s*Payment\s*Due\s+Minimum\s*Payment\s*Due\s+Statement\s*Period\s+Payment\s*Due\s*Date\s+Statement\s*Generation\s*Date\s*\n\s*([\d,]+\.\d{2})\s*Dr?\s+([\d,]+\.\d{2})\s*Dr?\s+(\d{2}\/\d{2}\/\d{4}\s*-\s*\d{2}\/\d{2}\/\d{4})\s+(\d{2}\/\d{2}\/\d{4})\s+(\d{2}\/\d{2}\/\d{4})",
        plumber_text,
        re.IGNORECASE
    )

    if table_match:
        details["new_balance"] = table_match.group(1).replace(",", "")
        details["min_amount_due"] = table_match.group(2).replace(",", "")
        details["billing_cycle"] = table_match.group(3)
        details["payment_due_date"] = table_match.group(4)
        details["statement_date"] = table_match.group(5)
        print("✅ Extracted Axis summary table data")

    #  Confidence Score
    filled = sum(1 for v in details.values() if v not in [None, ""])
    details["confidence"] = round(filled / len(details), 2)

    return details


def parse_axis_statement(file_path):
    pdf2_text = extract_text_pypdf2(file_path)
    plumber_text = extract_text_pdfplumber(file_path)

    data = extract_axis_details(pdf2_text, plumber_text)

    print("\n---- FINAL OUTPUT ----")
    print(json.dumps(data, indent=2))
    return data


# -------- Run --------
if __name__ == "__main__":
    file_path = r"examples\axis.pdf"
    parse_axis_statement(file_path)
