import re
import json
import os
from datetime import datetime
from base_extractor import extract_text_pypdf2
from hdfc_parser import parse_hdfc_statement
from axis_parser import parse_axis_statement
from icici_parser import parse_icici
from idfc_parser import parse_idfc_statement
from defence_parser import parse_defence_bank



def detect_bank(text):
    """Detect which bank the credit card statement belongs to."""
    text_upper = text.upper()
    if "HDFC BANK" in text_upper:
        return "HDFC"
    elif "AXIS BANK" in text_upper:
        return "AXIS"
    elif "ICICI BANK" in text_upper:
        return "ICICI"
    elif "IDFC" in text_upper:
        return "IDFC"
    elif "DEFENCE" in text_upper:
        return "DEFENCE"
    else:
        return "UNKNOWN"


def parse_credit_card_statement(file_path):
    """Auto-detect and parse credit card statement, save result as JSON."""
    text = extract_text_pypdf2(file_path)
    bank = detect_bank(text)

    print(f" Detected Bank: {bank}")

    if bank == "HDFC":
        result = parse_hdfc_statement(file_path)
    elif bank == "AXIS":
        result = parse_axis_statement(file_path)
    elif bank == "ICICI":
        result = parse_icici(file_path)
    elif bank == "IDFC":
        result = parse_idfc_statement(file_path)
    elif bank == "DEFENCE":
        result = parse_defence_bank(file_path)
    else:
        result = {"error": "Unsupported or unknown bank statement."}

    # --- Add metadata ---
    result["file_name"] = os.path.basename(file_path)
    result["parsed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- Save to JSON file ---
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(
        output_dir,
        f"{bank.lower()}_{os.path.splitext(os.path.basename(file_path))[0]}.json"
    )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Parsed data saved to: {output_path}")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    file_path = r"examples/idfc-2.pdf"  
    parse_credit_card_statement(file_path)
