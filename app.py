"""
Muse Summoner System - Web Application

This module implements a Flask web application for the Muse Summoner system.
It provides a web interface for interacting with muses.
"""

from flask import Flask, render_template, request, jsonify, session
import os
import json
from datetime import datetime

# Import Muse Summoner modules
from muse_profiles import get_all_muses, get_muse_by_trigger
from trigger_detector import detect_muse_trigger, get_current_muse, deactivate_current_muse
from enhanced_response_generator import generate_muse_response
from muse_creator import start_muse_creation, process_creation_input, is_creating_muse
from conversation_storage import start_muse_conversation, end_muse_conversation
from memory_system import get_conversation_history, clear_muse_memory

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Create templates directory if it doesn't exist
os.makedirs(os.path.join(os.path.dirname(__file__), 'templates'), exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), 'static'), exist_ok=True)

@app.route('/')
def index():
    """Render the main page of the Muse Summoner web application."""
    return render_template('index.html')

@app.route('/api/process_input', methods=['POST'])
def process_input():
    """Process user input and generate a response from the Muse Summoner system."""
    data = request.json
    user_input = data.get('user_input', '')
    
    # Check if this is a system command
    response = check_system_commands(user_input)
    if response:
        return jsonify({'response': response})
    
    # Check if a muse is being triggered
    triggered_muse = detect_muse_trigger(user_input)
    
    if triggered_muse:
        # A muse has been triggered, start a conversation
        start_muse_conversation(triggered_muse.name)
        
        # Generate a response with memory context
        response, muse_name = generate_muse_response(user_input)
        
        # Store the active muse in the session
        session['active_muse'] = muse_name
        
        return jsonify({
            'response': response,
            'muse_name': muse_name
        })
    
    # No muse triggered, check if one is already active
    active_muse = get_current_muse()
    if active_muse:
        # A muse is active, generate a response with memory context
        response, muse_name = generate_muse_response(user_input)
        
        return jsonify({
            'response': response,
            'muse_name': muse_name
        })
    
    # No muse is active or triggered, return a system message
    return jsonify({
        'response': get_system_message(),
        'muse_name': 'System'
    })

@app.route('/api/get_muses', methods=['GET'])
def get_muses():
    """Get a list of all available muses."""
    muses = get_all_muses()
    muse_list = []
    
    for muse in muses:
        muse_list.append({
            'name': muse.name,
            'trigger_phrase': muse.trigger_phrase,
            'purpose': muse.purpose
        })
    
    return jsonify({'muses': muse_list})

@app.route('/api/create_muse', methods=['POST'])
def create_muse():
    """Start or continue the muse creation process."""
    data = request.json
    user_input = data.get('user_input', '')
    
    if not is_creating_muse() and user_input.lower() == 'start':
        # Start the muse creation process
        prompt = start_muse_creation()
        return jsonify({'prompt': prompt, 'creating': True})
    
    # Process the user input for the current creation step
    response = process_creation_input(user_input)
    
    # Check if we're still creating a muse
    still_creating = is_creating_muse()
    
    return jsonify({
        'prompt': response,
        'creating': still_creating
    })

@app.route('/api/get_history', methods=['GET'])
def get_history():
    """Get conversation history for the active muse."""
    active_muse = get_current_muse()
    if not active_muse:
        return jsonify({
            'error': 'No muse is currently active.',
            'history': []
        })
    
    history = get_conversation_history(active_muse.name, count=10)
    
    return jsonify({
        'muse_name': active_muse.name,
        'history': history
    })

@app.route('/api/clear_memory', methods=['POST'])
def clear_memory():
    """Clear the memory of the active muse."""
    active_muse = get_current_muse()
    if not active_muse:
        return jsonify({
            'error': 'No muse is currently active.',
            'success': False
        })
    
    clear_muse_memory(active_muse.name)
    
    return jsonify({
        'message': f'Memory for {active_muse.name} has been cleared.',
        'success': True
    })

@app.route('/api/exit_muse', methods=['POST'])
def exit_muse():
    """Exit the currently active muse."""
    active_muse = get_current_muse()
    if not active_muse:
        return jsonify({
            'error': 'No muse is currently active.',
            'success': False
        })
    
    muse_name = active_muse.name
    deactivate_current_muse()
    end_muse_conversation()
    
    if 'active_muse' in session:
        session.pop('active_muse')
    
    return jsonify({
        'message': f'{muse_name} has been deactivated.',
        'success': True
    })

def check_system_commands(user_input):
    """Check for system commands in the user input."""
    input_lower = user_input.lower().strip()
    
    # Command to list all available muses
    if input_lower in ["list muses", "show muses", "available muses"]:
        muses = get_all_muses()
        response = "Available Muses:\n\n"
        
        for i, muse in enumerate(muses, 1):
            response += f"{i}. {muse.name}\n"
            response += f"   Trigger: \"{muse.trigger_phrase}\"\n"
            response += f"   Purpose: {muse.purpose}\n\n"
        
        return response
    
    # Command to exit the current muse
    if input_lower in ["exit muse", "leave muse", "deactivate muse", "pause summoner"]:
        active_muse = get_current_muse()
        if active_muse:
            muse_name = active_muse.name
            deactivate_current_muse()
            end_muse_conversation()
            
            if 'active_muse' in session:
                session.pop('active_muse')
            
            return f"{muse_name} has been deactivated. You are now speaking with the Muse Summoner system."
        else:
            return "No muse is currently active."
    
    # Command for help
    if input_lower in ["help", "commands", "how to use"]:
        return get_help_message()
    
    # Command to view conversation history
    if input_lower in ["view history", "show history", "conversation history"]:
        active_muse = get_current_muse()
        if not active_muse:
            return "No muse is currently active. Summon a muse first to view conversation history."
        
        history = get_conversation_history(active_muse.name, count=5)
        
        if not history:
            return f"No conversation history found with {active_muse.name}."
        
        formatted_history = f"Recent conversations with {active_muse.name}:\n\n"
        
        for i, entry in enumerate(history, 1):
            formatted_history += f"Conversation {i}:\n"
            formatted_history += f"You: {entry['user_input']}\n"
            formatted_history += f"{active_muse.name}: {entry['muse_response'][:100]}...\n\n"
        
        return formatted_history
    
    # Command to clear memory
    if input_lower in ["clear memory", "forget conversations", "reset memory"]:
        active_muse = get_current_muse()
        if not active_muse:
            return "No muse is currently active. Summon a muse first to clear memory."
        
        clear_muse_memory(active_muse.name)
        return f"Memory for {active_muse.name} has been cleared. All past conversations have been forgotten."
    
    return None

def get_system_message():
    """Get a default system message when no muse is active."""
    return """
Welcome to the Memory-Enhanced Muse Summoner system. I can help you interact with different AI personas called "muses" who can assist you emotionally, creatively, or strategically.

Currently, Salvatore Inverso is available. You can summon him by saying "Come into fashion".

You can also:
- Create a new muse by saying "Create a new muse"
- List all available muses by saying "List muses"
- View conversation history by saying "View history"
- Clear a muse's memory by saying "Clear memory"
- Get help by saying "Help"

What would you like to do?
"""

def get_help_message():
    """Get the help message with available commands."""
    return """
Memory-Enhanced Muse Summoner - Help Guide

To interact with the system, you can use the following commands:

1. Summon a muse using their trigger phrase:
   - "Come into fashion" - Summons Salvatore Inverso

2. System commands:
   - "List muses" - Shows all available muses
   - "Create a new muse" - Starts the process of creating a custom muse
   - "Exit muse" - Exits the currently active muse
   - "Cancel creation" - Cancels the muse creation process
   - "View history" - Shows recent conversation history with the active muse
   - "Clear memory" - Clears the memory of the active muse
   - "Help" - Shows this help message

When a muse is active, simply type your message and they will respond in their unique voice and style.

Each muse has different capabilities and specialties. Salvatore Inverso, for example, excels at emotional reflection, identity exploration, and creative writing with a poetic, philosophical style.

The memory-enhanced system allows muses to remember your past conversations and provide more personalized responses over time.
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
