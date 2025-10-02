from flask import Blueprint, request, jsonify, send_file, url_for
from config import Config

pass_bp = Blueprint('pass', __name__, url_prefix='/api')

@pass_bp.route('/generate', methods=['POST'])
def generate_pass():
    """Generate a new pass"""
    from app import pass_system
    
    data = request.json
    
    result = pass_system.create_pass(
        attendee_name=data['name'],
        ticket_type=data['ticketType'],
        event_name=data['eventName'],
        event_date=data['eventDate'],
        venue=data['venue']
    )
    
    return jsonify({
        "success": True,
        "serial_number": result['serial_number'],
        "id": result['id'],
        "pass_url": url_for('static', filename=f'passes/{result["filename"]}', _external=True)
    })

@pass_bp.route('/verify', methods=['POST'])
def verify_pass():
    """Verify and scan a pass"""
    from app import pass_system
    
    data = request.json
    serial_number = data.get('serial_number', '')
    result = pass_system.scan_pass(serial_number)
    return jsonify(result)

@pass_bp.route('/passes', methods=['GET'])
def get_all_passes():
    """Get all generated passes"""
    from app import pass_system
    
    passes = pass_system.get_all_passes()
    
    # Add URLs to passes
    for p in passes:
        p['pass_url'] = url_for('static', filename=f'passes/{p["serial_number"]}.png', _external=True)
    
    return jsonify({
        "success": True,
        "passes": passes,
        "total": len(passes)
    })

@pass_bp.route('/download/<serial>')
def download_pass(serial):
    """Download a pass"""
    filename = f"{serial}.png"
    filepath = Config.PASSES_DIR / filename
    return send_file(filepath, as_attachment=True)