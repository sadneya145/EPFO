from flask import Flask, render_template, jsonify, request, session
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'epfo_secret_key_2024'

# Mock Data
MOCK_USER = {
    "name": "Rajesh Kumar",
    "uan": "100XXXXXXXX",
    "dob": "15-Mar-1985",
    "company": "Tech Solutions Pvt. Ltd.",
    "mobile": "98XXXXXXXX",
    "email": "rajesh@example.com",
    "kyc_status": "Verified",
    "pf_balance": 284500,
    "employer_contribution": 142250,
    "employee_contribution": 142250,
    "last_credited": "Jan 2025"
}

MOCK_CONTRIBUTIONS = [
    {"month": "Aug", "employee": 4500, "employer": 4500},
    {"month": "Sep", "employee": 4500, "employer": 4500},
    {"month": "Oct", "employee": 4800, "employer": 4800},
    {"month": "Nov", "employee": 4800, "employer": 4800},
    {"month": "Dec", "employee": 5000, "employer": 5000},
    {"month": "Jan", "employee": 5200, "employer": 5200},
]

MOCK_CLAIMS = [
    {"id": "CLM2024001", "type": "PF Withdrawal", "amount": 50000, "status": "approved", "date": "12-Jan-2025", "step": 4},
    {"id": "CLM2024002", "type": "Pension Withdrawal", "amount": 30000, "status": "processing", "date": "20-Jan-2025", "step": 2},
    {"id": "CLM2024003", "type": "PF Transfer", "amount": 0, "status": "pending", "date": "25-Jan-2025", "step": 1},
]

MOCK_NOTIFICATIONS = [
    {"id": 1, "title": "KYC Verified", "message": "Your KYC documents have been verified successfully.", "time": "2 hours ago", "read": False, "type": "success"},
    {"id": 2, "title": "Claim Update", "message": "Your claim CLM2024001 has been approved.", "time": "1 day ago", "read": False, "type": "info"},
    {"id": 3, "title": "Contribution Credited", "message": "PF contribution for January 2025 has been credited.", "time": "3 days ago", "read": True, "type": "success"},
    {"id": 4, "title": "Session Reminder", "message": "Please update your nominee details.", "time": "1 week ago", "read": True, "type": "warning"},
]

MOCK_PASSBOOK = [
    {"date": "31-Jan-2025", "description": "Monthly Contribution", "employee_cr": 5200, "employer_cr": 5200, "balance": 284500},
    {"date": "31-Dec-2024", "description": "Monthly Contribution", "employee_cr": 5000, "employer_cr": 5000, "balance": 274100},
    {"date": "30-Nov-2024", "description": "Monthly Contribution", "employee_cr": 4800, "employer_cr": 4800, "balance": 264100},
    {"date": "31-Oct-2024", "description": "Monthly Contribution", "employee_cr": 4800, "employer_cr": 4800, "balance": 254500},
    {"date": "30-Sep-2024", "description": "Monthly Contribution", "employee_cr": 4500, "employer_cr": 4500, "balance": 244900},
    {"date": "31-Aug-2024", "description": "Monthly Contribution", "employee_cr": 4500, "employer_cr": 4500, "balance": 235900},
    {"date": "31-Jul-2024", "description": "Interest Credit", "employee_cr": 0, "employer_cr": 15000, "balance": 226900},
]

FAQ_DATA = [
    {"q": "How do I check my PF balance?", "a": "You can check your PF balance through the Member Portal by logging in with your UAN and password. Go to Dashboard → View Passbook."},
    {"q": "What documents are needed for KYC?", "a": "For KYC verification, you need: Aadhaar card, PAN card, Bank account details with IFSC code, and cancelled cheque."},
    {"q": "How long does a withdrawal claim take?", "a": "Online PF withdrawal claims are typically processed within 3-5 working days. Offline claims may take 15-20 working days."},
    {"q": "Can I transfer PF from old employer?", "a": "Yes, you can initiate PF transfer online through the Member Portal. Go to Online Services → Transfer Request and fill in your previous employer details."},
    {"q": "What is the interest rate on PF?", "a": "The current EPF interest rate is 8.15% per annum for 2023-24. Interest is calculated on monthly running balance and credited annually."},
    {"q": "How do I update my mobile number?", "a": "Visit any EPFO office with your UAN and Aadhaar card to update your mobile number, or use the UMANG app for online update."},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', user=MOCK_USER)

@app.route('/api/user')
def api_user():
    return jsonify(MOCK_USER)

@app.route('/api/contributions')
def api_contributions():
    return jsonify(MOCK_CONTRIBUTIONS)

@app.route('/api/claims')
def api_claims():
    return jsonify(MOCK_CLAIMS)

@app.route('/api/notifications')
def api_notifications():
    return jsonify(MOCK_NOTIFICATIONS)

@app.route('/api/passbook')
def api_passbook():
    return jsonify(MOCK_PASSBOOK)

@app.route('/api/faq')
def api_faq():
    return jsonify(FAQ_DATA)

@app.route('/api/search')
def api_search():
    query = request.args.get('q', '').lower()
    suggestions = [
        "Check PF Balance", "Download Passbook", "Track Claim Status",
        "Update KYC", "File PF Withdrawal", "Transfer PF", "View Contributions",
        "Update Nominee", "Change Password", "Pension Withdrawal",
        "Monthly Contribution History", "Generate UAN", "Link Aadhaar"
    ]
    results = [s for s in suggestions if query in s.lower()] if query else []
    return jsonify(results[:6])

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    if data.get('uan') and data.get('password'):
        return jsonify({"success": True, "redirect": "/dashboard"})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/api/claim/submit', methods=['POST'])
def submit_claim():
    data = request.json
    return jsonify({"success": True, "claim_id": "CLM2025001", "message": "Claim submitted successfully!"})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    msg = data.get('message', '').lower()
    responses = {
        'balance': "Your current PF balance is ₹2,84,500. Last credited: January 2025.",
        'claim': "You have 3 active claims. CLM2024001 is approved, CLM2024002 is processing.",
        'kyc': "Your KYC is fully verified. All documents are up to date.",
        'withdraw': "To withdraw PF, go to Online Services → Claim (Form-31/19/10C). You need verified KYC.",
        'transfer': "To transfer PF, go to Online Services → Transfer Request. You'll need your old employer's details.",
        'passbook': "Your passbook shows contributions from Aug 2024 to Jan 2025. Total balance: ₹2,84,500.",
    }
    for key, response in responses.items():
        if key in msg:
            return jsonify({"reply": response})
    return jsonify({"reply": "I can help you with PF balance, claims, KYC status, withdrawal, transfer, and passbook. What would you like to know?"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)