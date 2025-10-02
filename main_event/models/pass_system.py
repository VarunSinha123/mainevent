import hashlib
from datetime import datetime
from models.database import Database
from utils.qr_generator import QRGenerator
from utils.pass_designer import PassDesigner

class EventPassSystem:
    """Main event pass system orchestrator"""
    
    def __init__(self):
        self.db = Database()
        self.qr_gen = QRGenerator()
    
    def generate_hash_serial(self, attendee_name, ticket_type, sequential_num):
        """Generate unique serial number with sequential prefix"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        base = f"{attendee_name}{ticket_type}{timestamp}"
        hash_obj = hashlib.md5(base.encode())
        return f"NYE2025-{sequential_num:04d}-{hash_obj.hexdigest()[:6].upper()}"
    
    def create_pass(self, attendee_name, ticket_type, event_name, event_date, venue):
        """Create a new event pass"""
        # Get sequential serial number
        sequential_num = self.db.get_next_serial()
        serial_num = self.generate_hash_serial(attendee_name, ticket_type, sequential_num)
        
        pass_data = {
            "id": sequential_num,  # Sequential ID
            "serial_number": serial_num,
            "attendee_name": attendee_name,
            "ticket_type": ticket_type,
            "event_name": event_name,
            "event_date": event_date,
            "venue": venue,
            "issued_at": datetime.now().isoformat(),
            "status": "valid"
        }
        
        # Generate QR code
        qr_img = self.qr_gen.generate(pass_data)
        
        # Get sponsors and powered by info
        sponsors = self.db.get_all_sponsors()
        powered_by = self.db.get_powered_by()
        
        # Create pass design
        designer = PassDesigner(sponsors=sponsors, powered_by=powered_by)
        filename = designer.create_pass_image(pass_data, qr_img)
        
        # Save to database
        self.db.add_pass(pass_data)
        
        return {
            "serial_number": serial_num,
            "id": sequential_num,
            "filename": filename,
            "pass_data": pass_data
        }
    
    def verify_pass(self, serial_number):
        """Verify a pass without scanning"""
        pass_info = self.db.get_pass_by_serial(serial_number)
        
        if not pass_info:
            return {
                "valid": False,
                "message": "Invalid pass - Serial number not found",
                "details": None
            }
        
        if pass_info["status"] != "valid":
            return {
                "valid": False,
                "message": "Pass cancelled or invalid",
                "details": pass_info
            }
        
        scan_record = self.db.get_scan(serial_number)
        if scan_record:
            return {
                "valid": False,
                "message": "Pass already scanned",
                "details": pass_info,
                "scanned_at": scan_record["scanned_at"]
            }
        
        return {
            "valid": True,
            "message": "Valid pass - Entry granted",
            "details": pass_info
        }
    
    def scan_pass(self, serial_number):
        """Scan and verify a pass"""
        verification = self.verify_pass(serial_number)
        
        if verification["valid"]:
            self.db.add_scan(serial_number)
        
        return verification
    
    def get_all_passes(self):
        """Get all generated passes"""
        return self.db.get_all_passes()
    
    def get_stats(self):
        """Get system statistics"""
        return self.db.get_stats()
    
    def add_sponsor(self, name, logo_filename):
        """Add a new sponsor"""
        sponsor_data = {
            "name": name,
            "logo": logo_filename,
            "added_at": datetime.now().isoformat()
        }
        self.db.add_sponsor(sponsor_data)
        return True
    
    def get_sponsors(self):
        """Get all sponsors"""
        return self.db.get_all_sponsors()
    
    def remove_sponsor(self, name):
        """Remove a sponsor"""
        self.db.remove_sponsor(name)
        return True
    
    def update_powered_by(self, name, logo_filename):
        """Update powered by information"""
        self.db.update_powered_by(name, logo_filename)
        return True
    
    def get_powered_by(self):
        """Get powered by information"""
        return self.db.get_powered_by()