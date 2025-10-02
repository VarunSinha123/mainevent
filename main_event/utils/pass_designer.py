from PIL import Image, ImageDraw, ImageFont
from config import Config

class PassDesigner:
    """Create visual pass designs"""
    
    def __init__(self, sponsors=None, powered_by=None):
        self.sponsors = sponsors or []
        self.powered_by = powered_by or {}
        self.width = Config.PASS_WIDTH
        self.height = Config.PASS_HEIGHT
    
    def create_pass_image(self, pass_data, qr_img):
        """Create the complete pass image"""
        img = Image.new('RGB', (self.width, self.height), color='#F5EFE0')
        draw = ImageDraw.Draw(img)
        
        # Load fonts
        fonts = self._load_fonts()
        
        # Draw left section with QR
        self._draw_left_section(img, draw, qr_img, pass_data, fonts)
        
        # Draw right section with details
        self._draw_right_section(img, draw, pass_data, fonts)
        
        # Add powered by logo
        self._add_powered_by(img, draw, fonts)
        
        # Save and return filename
        filename = f"{pass_data['serial_number']}.png"
        filepath = Config.PASSES_DIR / filename
        img.save(filepath, quality=95)
        
        return filename
    
    def _load_fonts(self):
        """Load fonts with fallback"""
        try:
            return {
                'title': ImageFont.truetype("arial.ttf", 48),
                'year': ImageFont.truetype("arialbd.ttf", 120),
                'header': ImageFont.truetype("arial.ttf", 28),
                'body': ImageFont.truetype("arial.ttf", 22),
                'small': ImageFont.truetype("arial.ttf", 18),
                'tiny': ImageFont.truetype("arial.ttf", 14)
            }
        except:
            default = ImageFont.load_default()
            return {k: default for k in ['title', 'year', 'header', 'body', 'small', 'tiny']}
    
    def _draw_left_section(self, img, draw, qr_img, pass_data, fonts):
        """Draw left section with QR code"""
        left_width = 200
        
        # Background
        draw.rectangle([0, 0, left_width, self.height], fill='#E8DCC8')
        
        # QR code
        qr_size = 140
        qr_resized = qr_img.resize((qr_size, qr_size))
        qr_position = ((left_width - qr_size) // 2, 30)
        img.paste(qr_resized, qr_position)
        
        # Vertical "TICKET" text
        ticket_text = "TICKET"
        y_start = 190
        for i, char in enumerate(ticket_text):
            draw.text((left_width // 2, y_start + i * 25), 
                     char, fill='#8B7355', anchor='mm', font=fonts['small'])
        
        # Vertical event year
        event_year = "NEW YEAR"
        y_start = 310
        for i, char in enumerate(event_year):
            draw.text((left_width // 2, y_start + i * 12), 
                     char, fill='#8B7355', anchor='mm', font=fonts['tiny'])
        
        # Barcode-style decoration
        for i in range(5):
            x = 15 + i * 8
            draw.rectangle([x, self.height - 80, x + 3, self.height - 20], fill='#000000')
        
        # Serial number vertically
        serial_parts = pass_data['serial_number'].replace('-', '')
        for i, char in enumerate(serial_parts[:12]):
            draw.text((10, 30 + i * 28), char, fill='#000000', font=fonts['tiny'])
    
    def _draw_right_section(self, img, draw, pass_data, fonts):
        """Draw right section with event details"""
        right_start = 200
        
        # Black background
        draw.rectangle([right_start, 0, self.width, self.height], fill='#1a1a1a')
        
        # Party hat decorations
        hat_positions = [right_start + 180, self.width - 180]
        for hat_x in hat_positions:
            draw.polygon([(hat_x-25, 90), (hat_x, 40), (hat_x+25, 90)], fill='#D4AF37')
            draw.ellipse([hat_x-30, 85, hat_x+30, 95], fill='#FFFFFF')
            for dot_y in [50, 60, 70]:
                draw.ellipse([hat_x-3, dot_y, hat_x+3, dot_y+6], fill='#FFD700')
        
        center_x = (right_start + self.width) // 2
        
        # Event name
        draw.text((center_x, 60), pass_data['event_name'], 
                 fill='#D4AF37', anchor='mm', font=fonts['title'])
        
        # Year
        draw.text((center_x, 150), "2025", 
                 fill='#D4AF37', anchor='mm', font=fonts['year'])
        
        # Event details box
        draw.rectangle([right_start + 50, 220, self.width - 50, 250], 
                      outline='#D4AF37', width=2)
        draw.text((center_x, 235), f"{pass_data['event_date']} | START AT 8PM", 
                 fill='#FFFFFF', anchor='mm', font=fonts['body'])
        
        # Info section
        y_pos = 280
        draw.text((center_x, y_pos), f"📍 {pass_data['venue']}", 
                 fill='#FFFFFF', anchor='mm', font=fonts['small'])
        
        y_pos += 30
        draw.text((center_x, y_pos), f"👤 {pass_data['attendee_name']}", 
                 fill='#FFFFFF', anchor='mm', font=fonts['body'])
        
        y_pos += 28
        draw.text((center_x, y_pos), f"🎫 {pass_data['ticket_type']}", 
                 fill='#FFD700', anchor='mm', font=fonts['small'])
        
        # Add sponsors
        self._add_sponsors(img, draw, fonts)
        
        # Decorative dots
        for i in range(10):
            x = right_start + 100 + i * 90
            draw.ellipse([x, 15, x+4, 19], fill='#FFD700')
            draw.ellipse([x, self.height-19, x+4, self.height-15], fill='#FFD700')
    
    def _add_sponsors(self, img, draw, fonts):
        """Add multiple sponsor logos"""
        if not self.sponsors:
            return
        
        # Position sponsors at bottom right, stacked if multiple
        start_y = self.height - 80
        spacing = 50
        
        for i, sponsor in enumerate(self.sponsors[-3:]):  # Max 3 sponsors
            if not sponsor.get('logo'):
                continue
            
            try:
                logo_path = Config.SPONSORS_DIR / sponsor['logo']
                if not logo_path.exists():
                    continue
                
                sponsor_logo = Image.open(logo_path)
                logo_height = 35
                aspect = sponsor_logo.width / sponsor_logo.height
                logo_width = int(logo_height * aspect)
                sponsor_logo = sponsor_logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
                
                logo_x = self.width - logo_width - 60
                logo_y = start_y - (i * spacing)
                
                # White background
                draw.rectangle([logo_x - 5, logo_y - 5, 
                              logo_x + logo_width + 5, logo_y + logo_height + 5], 
                              fill='#FFFFFF')
                img.paste(sponsor_logo, (logo_x, logo_y), 
                         sponsor_logo if sponsor_logo.mode == 'RGBA' else None)
                
                # Sponsor label
                draw.text((logo_x - 80, logo_y + logo_height // 2), 
                         f"Sponsored by:", fill='#FFFFFF', anchor='rm', font=fonts['tiny'])
            except Exception as e:
                print(f"Error adding sponsor {sponsor.get('name')}: {e}")
    
    def _add_powered_by(self, img, draw, fonts):
        """Add 'Powered by' logo in top right"""
        if not self.powered_by.get('logo'):
            return
        
        try:
            logo_path = Config.POWERED_BY_DIR / self.powered_by['logo']
            if not logo_path.exists():
                return
            
            powered_logo = Image.open(logo_path)
            logo_height = 30
            aspect = powered_logo.width / powered_logo.height
            logo_width = int(logo_height * aspect)
            powered_logo = powered_logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
            
            # Position at top right
            logo_x = self.width - logo_width - 20
            logo_y = 10
            
            # Semi-transparent white background
            draw.rectangle([logo_x - 5, logo_y - 5, 
                          logo_x + logo_width + 5, logo_y + logo_height + 5], 
                          fill='#FFFFFF')
            img.paste(powered_logo, (logo_x, logo_y), 
                     powered_logo if powered_logo.mode == 'RGBA' else None)
            
            # "Powered by" text
            draw.text((logo_x - 85, logo_y + logo_height // 2), 
                     "Powered by", fill='#FFFFFF', anchor='rm', font=fonts['tiny'])
        except Exception as e:
            print(f"Error adding powered by logo: {e}")