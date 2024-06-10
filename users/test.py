

import qrcode
from qr_pay import QRPay

# Tạo đối tượng QRPay
data = {
    "bin_id": "970415",
    "consumer_id": "101879621882",
    'purpose_of_transaction':"Thanh toan hoa don",
    "transaction_amount": 200000
}
qr_pay = QRPay(**data)
# Lấy mã QR
qr_code_data = qr_pay.code

# Tạo mã QR
qr = qrcode.make(qr_code_data)

# Hiển thị mã QR
qr.show()
