import qrcode

url = "https://event-backend-m5oh.onrender.com/demo"

qr = qrcode.make(url)
qr.save("event_qr.png")

print("QR ready")