import json
from pathlib import Path
from datetime import datetime
from config import Config

class Database:
    """Handle all database operations"""
    
    def __init__(self):
        self.db_file = Config.DATABASE_FILE
        self._load()
    
    def _load(self):
        """Load database from file"""
        if self.db_file.exists():
            with open(self.db_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "passes": [],
                "scanned": [],
                "sponsors": [],
                "powered_by": {
                    "name": Config.POWERED_BY_NAME,
                    "logo": Config.POWERED_BY_LOGO
                },
                "next_serial": 1  # Sequential counter
            }
            self._save()
    
    def _save(self):
        """Save database to file"""
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get_next_serial(self):
        """Get next sequential serial number"""
        serial = self.data.get("next_serial", 1)
        self.data["next_serial"] = serial + 1
        self._save()
        return serial
    
    def add_pass(self, pass_data):
        """Add a new pass to database"""
        self.data["passes"].append(pass_data)
        self._save()
    
    def get_all_passes(self):
        """Get all passes"""
        return self.data["passes"]
    
    def get_pass_by_serial(self, serial_number):
        """Get pass by serial number"""
        for p in self.data["passes"]:
            if p["serial_number"] == serial_number:
                return p
        return None
    
    def add_scan(self, serial_number):
        """Record a pass scan"""
        self.data["scanned"].append({
            "serial_number": serial_number,
            "scanned_at": datetime.now().isoformat()
        })
        self._save()
    
    def get_scan(self, serial_number):
        """Get scan record for a pass"""
        for scan in self.data["scanned"]:
            if scan["serial_number"] == serial_number:
                return scan
        return None
    
    def get_all_scans(self):
        """Get all scanned passes"""
        return self.data["scanned"]
    
    def add_sponsor(self, sponsor_data):
        """Add a sponsor"""
        self.data["sponsors"].append(sponsor_data)
        self._save()
    
    def get_all_sponsors(self):
        """Get all sponsors"""
        return self.data["sponsors"]
    
    def remove_sponsor(self, sponsor_name):
        """Remove a sponsor by name"""
        self.data["sponsors"] = [s for s in self.data["sponsors"] if s["name"] != sponsor_name]
        self._save()
    
    def update_powered_by(self, name, logo):
        """Update powered by information"""
        self.data["powered_by"] = {
            "name": name,
            "logo": logo,
            "updated_at": datetime.now().isoformat()
        }
        self._save()
    
    def get_powered_by(self):
        """Get powered by information"""
        return self.data.get("powered_by", {
            "name": Config.POWERED_BY_NAME,
            "logo": Config.POWERED_BY_LOGO
        })
    
    def get_stats(self):
        """Get statistics"""
        total = len(self.data["passes"])
        scanned = len(self.data["scanned"])
        return {
            "total": total,
            "scanned": scanned,
            "pending": total - scanned,
            "attendance_rate": round((scanned/total*100), 1) if total > 0 else 0
        }