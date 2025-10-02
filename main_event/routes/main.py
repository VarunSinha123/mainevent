from flask import Blueprint, render_template, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Homepage"""
    return render_template('index.html')

@main_bp.route('/generate')
def generate_page():
    """Pass generation page"""
    return render_template('generate.html')

@main_bp.route('/scan')
def scan_page():
    """Pass scanning page"""
    return render_template('scan.html')

@main_bp.route('/sponsor')
def sponsor_page():
    """Sponsor management page"""
    return render_template('sponsor.html')

@main_bp.route('/view-passes')
def view_passes_page():
    """View all generated passes"""
    return render_template('view_passes.html')

@main_bp.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics API"""
    from app import pass_system
    stats = pass_system.get_stats()
    return jsonify(stats)