import requests
import json


def ocr(file):
    print("=== Python Receipt OCR Demo - Need help? Email support@asprise.com ===")

    # Receipt OCR API endpoint
    receiptOcrEndpoint = 'https://ocr.asprise.com/api/v1/receipt'
    imageFile = file  # // Modify this to use your own file if necessary
    print('RECEIPT NAME:', imageFile)
    receipt = requests.post(receiptOcrEndpoint, data={
        'client_id': 'TEST',        # Use 'TEST' for testing purpose \
        'recognizer': 'auto',       # can be 'US', 'CA', 'JP', 'SG' or 'auto' \
        'ref_no': 'ocr_python_123'  # optional caller provided ref code \
    }, \
        files={"file": open(file, "rb")})

    receipt_decoded = json.loads(receipt.text)  # result in JSON
    print(receipt_decoded)
