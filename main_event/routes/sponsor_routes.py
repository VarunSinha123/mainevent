from flask import Blueprint, request, jsonify, url_for
from datetime import datetime
from config import Config

sponsor_bp = Blueprint('sponsor', __name__, url_prefix='/api')

@sponsor_bp.route('/sponsor', methods=['POST'])
def add_sponsor():
    """Add a new sponsor"""
    from app import pass_system
    
    try:
        name = request.form.get('name')
        logo = request.files.get('logo')
        
        if not name or not logo:
            return jsonify({"success": False, "message": "Name and logo required"})
        
        # Save logo
        filename = f"sponsor_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        logo_path = Config.SPONSORS_DIR / filename
        logo.save(logo_path)
        
        # Add to database
        pass_system.add_sponsor(name, filename)
        
        return jsonify({"success": True, "message": "Sponsor added successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@sponsor_bp.route('/sponsor', methods=['GET'])
def get_sponsors():
    """Get all sponsors"""
    from app import pass_system
    
    sponsors = pass_system.get_sponsors()
    
    # Add URLs
    for sponsor in sponsors:
        sponsor['logo_url'] = url_for('static', filename=f'sponsors/{sponsor["logo"]}', _external=True)
    
    return jsonify({
        "success": True,
        "sponsors": sponsors
    })

@sponsor_bp.route('/sponsor/<name>', methods=['DELETE'])
def remove_sponsor(name):
    """Remove a sponsor"""
    from app import pass_system
    
    try:
        pass_system.remove_sponsor(name)
        return jsonify({"success": True, "message": "Sponsor removed"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@sponsor_bp.route('/powered-by', methods=['POST'])
def update_powered_by():
    """Update powered by information"""
    from app import pass_system
    
    try:
        name = request.form.get('name')
        logo = request.files.get('logo')
        
        if not name or not logo:
            return jsonify({"success": False, "message": "Name and logo required"})
        
        # Save logo
        filename = f"powered_by_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        logo_path = Config.POWERED_BY_DIR / filename
        logo.save(logo_path)
        
        # Update database
        pass_system.update_powered_by(name, filename)
        
        return jsonify({"success": True, "message": "Powered by updated successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@sponsor_bp.route('/powered-by', methods=['GET'])
def get_powered_by():
    """Get powered by information"""
    from app import pass_system
    
    powered_by = pass_system.get_powered_by()
    
    if powered_by and powered_by.get('logo'):
        powered_by['logo_url'] = url_for('static', filename=f'powered_by/{powered_by["logo"]}', _external=True)
    
    return jsonify(powered_by if powered_by else {})