"""
Muse Summoner System - Admin Interface

This module implements an admin interface for customizing the Muse Summoner system.
It provides web routes for modifying configuration, managing muses, and viewing system status.
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import os
import json
from config import get_config, set_config, save_config, reset_config
from muse_profiles import get_all_muses, get_muse_by_name
from memory_system import clear_muse_memory

# Create a Blueprint for the admin routes
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def admin_home():
    """Render the admin dashboard."""
    return render_template('admin/dashboard.html')

@admin_bp.route('/config')
def admin_config():
    """Render the configuration page."""
    config = get_config()
    return render_template('admin/config.html', config=config)

@admin_bp.route('/config/update', methods=['POST'])
def update_config():
    """Update system configuration."""
    data = request.json
    
    for key, value in data.items():
        set_config(key, value)
    
    success = save_config()
    
    return jsonify({
        'success': success,
        'message': 'Configuration updated successfully' if success else 'Error updating configuration'
    })

@admin_bp.route('/config/reset', methods=['POST'])
def admin_reset_config():
    """Reset configuration to defaults."""
    success = reset_config()
    
    return jsonify({
        'success': success,
        'message': 'Configuration reset to defaults' if success else 'Error resetting configuration'
    })

@admin_bp.route('/muses')
def admin_muses():
    """Render the muse management page."""
    muses = get_all_muses()
    return render_template('admin/muses.html', muses=muses)

@admin_bp.route('/muses/<muse_name>')
def admin_muse_detail(muse_name):
    """Render the muse detail page."""
    muse = get_muse_by_name(muse_name)
    
    if not muse:
        return redirect(url_for('admin.admin_muses'))
    
    return render_template('admin/muse_detail.html', muse=muse)

@admin_bp.route('/muses/<muse_name>/clear_memory', methods=['POST'])
def admin_clear_muse_memory(muse_name):
    """Clear memory for a specific muse."""
    muse = get_muse_by_name(muse_name)
    
    if not muse:
        return jsonify({
            'success': False,
            'message': f'Muse {muse_name} not found'
        })
    
    clear_muse_memory(muse.name)
    
    return jsonify({
        'success': True,
        'message': f'Memory for {muse.name} has been cleared'
    })

@admin_bp.route('/system')
def admin_system():
    """Render the system status page."""
    # Get system information
    memory_dir = get_config('memory_storage_dir', 'memory')
    memory_files = []
    
    if os.path.exists(memory_dir):
        memory_files = [f for f in os.listdir(memory_dir) if f.endswith('_memory.json')]
    
    system_info = {
        'memory_files': memory_files,
        'muse_count': len(get_all_muses()),
        'config_file': os.path.exists('config.json')
    }
    
    return render_template('admin/system.html', system_info=system_info)

@admin_bp.route('/export', methods=['GET'])
def admin_export():
    """Export system data."""
    # Get all muses
    muses = get_all_muses()
    muse_data = []
    
    for muse in muses:
        muse_data.append(muse.to_dict())
    
    # Get configuration
    config = get_config()
    
    # Combine data
    export_data = {
        'muses': muse_data,
        'config': config
    }
    
    return jsonify(export_data)

@admin_bp.route('/import', methods=['POST'])
def admin_import():
    """Import system data."""
    try:
        data = request.json
        
        # Import configuration
        if 'config' in data:
            for key, value in data['config'].items():
                set_config(key, value)
            save_config()
        
        # Import muses (would need additional implementation)
        # This is a placeholder for future implementation
        
        return jsonify({
            'success': True,
            'message': 'Data imported successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error importing data: {str(e)}'
        })

# Function to register the admin blueprint with the Flask app
def register_admin_blueprint(app):
    """Register the admin blueprint with the Flask app."""
    app.register_blueprint(admin_bp)
    
    # Create admin template directories if they don't exist
    os.makedirs(os.path.join(os.path.dirname(__file__), 'templates/admin'), exist_ok=True)
