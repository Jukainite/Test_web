

import qrcode
from qr_pay import QRPay

def QR(content, amount):
    # Tạo đối tượng QRPay
    data = {
        "bin_id": "970436",
        "consumer_id": "1016266506",
        'purpose_of_transaction':content,
        "transaction_amount": amount
    }
    qr_pay = QRPay(**data)
    # Lấy mã QR
    qr_code_data = qr_pay.code

    # Tạo mã QR
    qr = qrcode.make(qr_code_data)
    return qr
# # Hiển thị mã QR
# qr.show()
