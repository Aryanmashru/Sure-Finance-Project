import re
import pdfplumber

def extract_text_pdfplumber(pdf_path):
    """Extract full text from a PDF using pdfplumber."""
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
    return full_text


def parse_icici(pdf_path):
    text = extract_text_pdfplumber(pdf_path)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    text_flat = " ".join(lines)  # fallback for single-line regex

    result = {
        "bank": "ICICI",
        "card_last4": None,
        "statement_date": None,
        "payment_due_date": None,
        "new_balance": None,
        "min_amount_due": None,
        "billing_cycle": None,
        "confidence": 0.0
    }

    # ------------------ CARD NUMBER ------------------
    card_match = re.search(
        r'(?:\d{4}\s*[Xx*]{2,}\s*[Xx*]{2,}\s*[Xx*]{2,}\s*(\d{4}))|(?:[Xx*]{4}\s*[Xx*]{4}\s*[Xx*]{4}\s*(\d{4}))',
        text_flat
    )
    if card_match:
        result["card_last4"] = card_match.group(1) or card_match.group(2)

    # ------------------ STATEMENT DATE ------------------
    stmt_pattern = re.search(
        r"STATEMENT\s*DATE\s*[:\-]?\s*([A-Za-z]+\s*\d{1,2},?\s*\d{4})",
        text_flat, re.IGNORECASE)
    if stmt_pattern:
        result["statement_date"] = stmt_pattern.group(1)

    # ------------------ PAYMENT DUE DATE ------------------
    due_pattern = re.search(
        r"PAYMENT\s*DUE\s*DATE\s*[:\-]?\s*([A-Za-z]+\s*\d{1,2},?\s*\d{4})",
        text_flat, re.IGNORECASE)
    if due_pattern:
        result["payment_due_date"] = due_pattern.group(1)

    # ------------------ TOTAL AMOUNT DUE (multi-line safe) ------------------
    for i, line in enumerate(lines):
        if re.search(r"Total\s*Amount\s*Due", line, re.I):
            if i + 1 < len(lines):
                next_match = re.search(r"([\d,]+\.\d{2})", lines[i + 1])
                if next_match:
                    result["new_balance"] = next_match.group(1).replace(",", "")

    # ------------------ MINIMUM AMOUNT DUE (multi-line safe) ------------------
    for i, line in enumerate(lines):
        if re.search(r"Minimum\s*Amount\s*Due", line, re.I):
            match = re.search(r"([\d,]+\.\d{2})", line)
            if match:
                result["min_amount_due"] = match.group(1).replace(",", "")
            elif i + 1 < len(lines):
                next_match = re.search(r"([\d,]+\.\d{2})", lines[i + 1])
                if next_match:
                    result["min_amount_due"] = next_match.group(1).replace(",", "")

    # ------------------ BILLING CYCLE ------------------
    billing_pattern = re.search(
        r"(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})\s*(?:to|-|–)\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})", text_flat)
    if billing_pattern:
        result["billing_cycle"] = f"{billing_pattern.group(1)} - {billing_pattern.group(2)}"

    # ------------------ CONFIDENCE ------------------
    fields = [result[k] for k in result if k not in ["bank", "confidence"]]
    filled = sum(1 for v in fields if v)
    result["confidence"] = round(filled / len(fields), 2)

    print("\nDetected: ICICI Bank Statement ✅")
    print(result)
    return result


if __name__ == "__main__":
    pdf_path = "examples/icici-3.pdf"  # <— place your ICICI PDF path here
    parse_icici(pdf_path)
