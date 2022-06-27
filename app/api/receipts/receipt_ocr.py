import requests
import json


def receipt_ocr(file):
    print("=== Python Receipt OCR Demo - Need help? Email support@asprise.com ===")

    # Receipt OCR API endpoint
    receiptOcrEndpoint = 'https://ocr.asprise.com/api/v1/receipt'
    data = requests.post(receiptOcrEndpoint, data={
        'client_id': 'TEST',        # Use 'TEST' for testing purpose \
        'recognizer': 'auto',       # can be 'US', 'CA', 'JP', 'SG' or 'auto' \
        'ref_no': 'ocr_python_123'  # optional caller provided ref code \
    }, \
        files={"file": open(file.filename, "rb")})

    receipt = json.loads(data.text)  # result in JSON
<<<<<<< HEAD
    print(type(receipt), receipt)
=======
    print(type(receipt), receipt['receipts'])
    return receipt['receipts']
>>>>>>> 72bdfc1 (updated root directory)
