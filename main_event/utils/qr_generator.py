import qrcode
import json

class QRGenerator:
    """Generate QR codes for passes"""
    
    @staticmethod
    def generate(pass_data):
        """Generate QR code image from pass data"""
        qr_data = json.dumps({
            "serial": pass_data["serial_number"],
            "event": pass_data["event_name"],
            "name": pass_data["attendee_name"]
        })
        
        qr = qrcode.QRCode(version=1, box_size=8, border=2)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        return qr.make_image(fill_color="black", back_color="white")