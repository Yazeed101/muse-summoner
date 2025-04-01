"""
Admin API with Authentication for Muse Summoner System

This module implements a secure API for remote administration of the Muse Summoner system.
It includes authentication, authorization, and endpoints for system management.
"""

from flask import Blueprint, request, jsonify, current_app
import os
import json
import secrets
import hashlib
import time
from functools import wraps
from config import get_config, set_config, save_config
from muse_profiles import get_all_muses, get_muse_by_name
from memory_system import clear_muse_memory

# Create a Blueprint for the admin API routes
admin_api_bp = Blueprint('admin_api', __name__, url_prefix='/api/admin')

# API keys storage
API_KEYS_FILE = 'api_keys.json'

def load_api_keys():
    """Load API keys from file."""
    if os.path.exists(API_KEYS_FILE):
        try:
            with open(API_KEYS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_api_keys(api_keys):
    """Save API keys to file."""
    with open(API_KEYS_FILE, 'w') as f:
        json.dump(api_keys, f, indent=2)

def generate_api_key(username, role='admin'):
    """Generate a new API key for a user."""
    api_keys = load_api_keys()
    
    # Generate a secure random token
    token = secrets.token_hex(32)
    
    # Store the API key with user info and creation timestamp
    api_keys[token] = {
        'username': username,
        'role': role,
        'created_at': time.time()
    }
    
    save_api_keys(api_keys)
    return token

def verify_api_key(api_key):
    """Verify if an API key is valid."""
    api_keys = load_api_keys()
    return api_key in api_keys

def get_user_from_api_key(api_key):
    """Get user information from an API key."""
    api_keys = load_api_keys()
    if api_key in api_keys:
        return api_keys[api_key]
    return None

def revoke_api_key(api_key):
    """Revoke an API key."""
    api_keys = load_api_keys()
    if api_key in api_keys:
        del api_keys[api_key]
        save_api_keys(api_keys)
        return True
    return False

# Authentication decorator
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get API key from Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'Missing or invalid Authorization header'
            }), 401
        
        api_key = auth_header.split('Bearer ')[1]
        
        if not verify_api_key(api_key):
            return jsonify({
                'success': False,
                'error': 'Invalid API key'
            }), 401
        
        # Add user info to request
        request.user = get_user_from_api_key(api_key)
        
        return f(*args, **kwargs)
    return decorated_function

# API Routes

@admin_api_bp.route('/auth', methods=['POST'])
def authenticate():
    """Authenticate a user and generate an API key."""
    data = request.json
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({
            'success': False,
            'error': 'Missing username or password'
        }), 400
    
    username = data['username']
    password = data['password']
    
    # In a real system, you would verify against a database
    # For this example, we'll use a hardcoded admin user
    admin_username = get_config('admin_username', 'admin')
    admin_password_hash = get_config('admin_password_hash', hashlib.sha256('admin'.encode()).hexdigest())
    
    # Hash the provided password
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if username == admin_username and password_hash == admin_password_hash:
        # Generate and return an API key
        api_key = generate_api_key(username)
        
        return jsonify({
            'success': True,
            'api_key': api_key,
            'user': {
                'username': username,
                'role': 'admin'
            }
        })
    
    return jsonify({
        'success': False,
        'error': 'Invalid username or password'
    }), 401

@admin_api_bp.route('/auth/revoke', methods=['POST'])
@require_api_key
def revoke_token():
    """Revoke the current API key."""
    auth_header = request.headers.get('Authorization')
    api_key = auth_header.split('Bearer ')[1]
    
    success = revoke_api_key(api_key)
    
    return jsonify({
        'success': success,
        'message': 'API key revoked successfully' if success else 'Failed to revoke API key'
    })

@admin_api_bp.route('/config', methods=['GET'])
@require_api_key
def get_config_api():
    """Get the current system configuration."""
    config = get_config()
    
    # Remove sensitive information
    if 'admin_password_hash' in config:
        del config['admin_password_hash']
    
    return jsonify({
        'success': True,
        'config': config
    })

@admin_api_bp.route('/config', methods=['PUT'])
@require_api_key
def update_config_api():
    """Update system configuration."""
    data = request.json
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No configuration data provided'
        }), 400
    
    # Update configuration
    for key, value in data.items():
        set_config(key, value)
    
    # Save configuration
    success = save_config()
    
    return jsonify({
        'success': success,
        'message': 'Configuration updated successfully' if success else 'Failed to update configuration'
    })

@admin_api_bp.route('/muses', methods=['GET'])
@require_api_key
def get_muses_api():
    """Get all available muses."""
    muses = get_all_muses()
    muse_list = []
    
    for muse in muses:
        muse_list.append({
            'name': muse.name,
            'trigger_phrase': muse.trigger_phrase,
            'purpose': muse.purpose,
            'voice_tone': muse.voice_tone,
            'tasks_supported': muse.tasks_supported,
            'catchphrases': muse.catchphrases,
            'signature_question': muse.signature_question
        })
    
    return jsonify({
        'success': True,
        'muses': muse_list
    })

@admin_api_bp.route('/muses/<muse_name>', methods=['GET'])
@require_api_key
def get_muse_api(muse_name):
    """Get details for a specific muse."""
    muse = get_muse_by_name(muse_name)
    
    if not muse:
        return jsonify({
            'success': False,
            'error': f'Muse {muse_name} not found'
        }), 404
    
    muse_data = {
        'name': muse.name,
        'trigger_phrase': muse.trigger_phrase,
        'purpose': muse.purpose,
        'voice_tone': muse.voice_tone,
        'tasks_supported': muse.tasks_supported,
        'catchphrases': muse.catchphrases,
        'signature_question': muse.signature_question,
        'sample_tasks': muse.sample_tasks,
        'ritual_system': muse.ritual_system
    }
    
    return jsonify({
        'success': True,
        'muse': muse_data
    })

@admin_api_bp.route('/muses/<muse_name>/memory', methods=['DELETE'])
@require_api_key
def clear_muse_memory_api(muse_name):
    """Clear memory for a specific muse."""
    muse = get_muse_by_name(muse_name)
    
    if not muse:
        return jsonify({
            'success': False,
            'error': f'Muse {muse_name} not found'
        }), 404
    
    clear_muse_memory(muse.name)
    
    return jsonify({
        'success': True,
        'message': f'Memory for {muse.name} has been cleared'
    })

@admin_api_bp.route('/system/status', methods=['GET'])
@require_api_key
def system_status_api():
    """Get system status information."""
    # Get system information
    memory_dir = get_config('memory_storage_dir', 'memory')
    memory_files = []
    
    if os.path.exists(memory_dir):
        memory_files = [f for f in os.listdir(memory_dir) if f.endswith('_memory.json')]
    
    system_info = {
        'memory_files': memory_files,
        'muse_count': len(get_all_muses()),
        'config_file': os.path.exists('config.json'),
        'version': '1.0.0',
        'uptime': time.time()  # In a real system, you would track actual uptime
    }
    
    return jsonify({
        'success': True,
        'system_info': system_info
    })

# Function to register the admin API blueprint with the Flask app
def register_admin_api_blueprint(app):
    """Register the admin API blueprint with the Flask app."""
    app.register_blueprint(admin_api_bp)
    
    # Create initial admin user if it doesn't exist
    if 'admin_username' not in get_config() or 'admin_password_hash' not in get_config():
        set_config('admin_username', 'admin')
        set_config('admin_password_hash', hashlib.sha256('admin'.encode()).hexdigest())
        save_config()
