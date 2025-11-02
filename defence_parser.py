import re
import json
from base_extractor import extract_text_pypdf2

def parse_defence_bank(pdf_path):
    text = extract_text_pypdf2(pdf_path)
    text = text.replace("\n", " ").replace("  ", " ")

    details = {
        "bank": "DEFENCE",
        "card_last4": None,
        "statement_date": None,
        "payment_due_date": None,
        "new_balance": None,
        "min_amount_due": None,
        "billing_cycle": None,
        "confidence": 0.0
    }

    # 🔹 Extract Billing Cycle
    match_period = re.search(
        r"Statement\s*Period\s*[:\-]?\s*([A-Za-z0-9\s]+?)[\-–]\s*([A-Za-z0-9\s]+?)\b",
        text, re.IGNORECASE
    )
    if match_period:
        start = match_period.group(1).strip()
        end = match_period.group(2).strip()
        details["billing_cycle"] = f"{start} - {end}"
        details["statement_date"] = end

    # 🔹 Extract Payment Due Date
    match_due = re.search(
        r"Payment\s*Due\s*Date\s*[:\-]?\s*([0-9]{1,2}\s*[A-Za-z]{3,9}\s*[0-9]{2,4})",
        text, re.IGNORECASE
    )
    if match_due:
        details["payment_due_date"] = match_due.group(1).strip()

    # 🔹 Extract Minimum Amount Due
    match_min = re.search(
        r"Minimum\s*Payment\s*[:\-]?\s*[\$₹]?\s*([0-9,]+\.\d{2})",
        text, re.IGNORECASE
    )
    if match_min:
        details["min_amount_due"] = match_min.group(1).strip()

    # 🔹 Extract Total Payment Due
    match_total = re.search(
        r"Total\s*Payment\s*Due\s*[:\-]?\s*[\$₹]?\s*([0-9,]+\.\d{2})",
        text, re.IGNORECASE
    )
    if match_total:
        details["new_balance"] = match_total.group(1).strip()

    # 🔹 Extract Card Number
    match_card = re.search(r"(\d{4})\s*\*{4,}\s*(\d{4})", text)
    if match_card:
        details["card_last4"] = match_card.group(2).strip()

    # 🔹 Clean unwanted trailing words
    for key in ["statement_date", "payment_due_date"]:
        if details[key]:
            details[key] = re.split(r"\s+(Statement|Minimum|Page|Cardholder)\b", details[key])[0].strip()

    # 🔹 Confidence
    filled = sum(v not in [None, ""] for k, v in details.items() if k not in ["bank", "confidence"])
    details["confidence"] = round(filled / 6, 2)

    print("Detected: DEFENCE Bank Statement ✅\n")
    print(json.dumps(details, indent=2))
    return details


# -------- Run --------
if __name__ == "__main__":
    pdf_path = r"examples\defence.pdf"  # Replace with your Defence Bank statement
    parse_defence_bank(pdf_path)
