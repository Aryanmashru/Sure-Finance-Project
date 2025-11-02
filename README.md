# Credit Card Statement Parser

A modular and heuristics Python-based system to automatically detect and extract data from credit card statements across multiple banks (HDFC, Axis, ICICI, IDFC, Defence).

##  Features
- Auto-detects bank type using text analysis
- Extracts key fields like:
  - Statement Date
  - Payment Due Date
  - Total Amount Due
  - Minimum Amount Due
  - Last 4 Digits of Card
  - Billing Cycle
- Confidence score based on filled fields
- Modular architecture for easy addition of new banks

##  Supported Banks
✅ HDFC  
✅ Axis  
✅ ICICI  
✅ IDFC  
✅ Defence  


## How to Run

```bash
#Clone Repo
git clone <https://github.com/Aryanmashru/Sure-Finance-Project.git>
cd <Sure-Finance-Project>

# Install dependencies
pip install -r requirements.txt

# Run parser
python main_parser.py #Change the file in the main_parser.py and run the file through terminal 
