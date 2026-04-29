import qrcode

# 🔥 UPDATE THIS AFTER RENDER DEPLOYS
url = "https://event-backend.onrender.com/demo"

qr = qrcode.make(url)
qr.save("event_qr.png")

print("✅ QR generated: event_qr.png")