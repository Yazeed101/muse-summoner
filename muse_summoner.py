"""
Muse Summoner System - Updated Main Application

This is the updated main module that integrates all components of the Muse Summoner system,
including the new memory and conversation storage features.
"""

import re
from muse_profiles import get_all_muses, get_muse_by_trigger
from trigger_detector import detect_muse_trigger, get_current_muse, deactivate_current_muse, extract_user_task
from enhanced_response_generator import generate_muse_response
from muse_creator import start_muse_creation, process_creation_input, is_creating_muse, cancel_muse_creation, get_muse_list_formatted
from conversation_storage import start_muse_conversation, end_muse_conversation, is_muse_conversation_active, get_active_muse
from memory_system import clear_muse_memory, get_conversation_history

class MuseSummoner:
    def __init__(self):
        self.creating_muse = False
    
    def process_input(self, user_input):
        """
        Process user input and generate appropriate responses.
        This is the main entry point for the Muse Summoner system.
        """
        # Check if we're in the process of creating a new muse
        if is_creating_muse():
            return process_creation_input(user_input)
        
        # Check for system commands
        system_response = self._check_system_commands(user_input)
        if system_response:
            return system_response
        
        # Check if a muse is being triggered
        triggered_muse = detect_muse_trigger(user_input)
        
        if triggered_muse:
            # A muse has been triggered, start a conversation if not already active
            if not is_muse_conversation_active() or get_active_muse() != triggered_muse.name:
                start_muse_conversation(triggered_muse.name)
            
            # Generate a response with memory context
            response, muse_name = generate_muse_response(user_input)
            return response
        
        # No muse triggered, check if one is already active
        active_muse = get_current_muse()
        if active_muse:
            # A muse is active, generate a response with memory context
            response, muse_name = generate_muse_response(user_input)
            return response
        
        # No muse is active or triggered, return a system message
        return self._get_system_message()
    
    def _check_system_commands(self, user_input):
        """Check for system commands in the user input."""
        # Convert to lowercase for case-insensitive matching
        input_lower = user_input.lower().strip()
        
        # Command to list all available muses
        if re.search(r'\b(list muses|show muses|available muses)\b', input_lower):
            return get_muse_list_formatted()
        
        # Command to create a new muse
        if re.search(r'\b(create (a )?new muse|add (a )?muse|new muse)\b', input_lower):
            return start_muse_creation()
        
        # Command to exit the current muse
        if re.search(r'\b(exit muse|leave muse|deactivate muse)\b', input_lower):
            if get_current_muse():
                muse_name = get_current_muse().name
                deactivate_current_muse()
                end_muse_conversation()
                return f"{muse_name} has been deactivated. You are now speaking with the Muse Summoner system."
            else:
                return "No muse is currently active."
        
        # Command to cancel muse creation
        if re.search(r'\b(cancel creation|stop creating|abort creation)\b', input_lower):
            return cancel_muse_creation()
        
        # Command for help
        if input_lower in ["help", "commands", "how to use"]:
            return self._get_help_message()
        
        # Command to view conversation history
        if re.search(r'\b(view history|show history|conversation history)\b', input_lower):
            return self._get_conversation_history()
        
        # Command to clear memory
        if re.search(r'\b(clear memory|forget conversations|reset memory)\b', input_lower):
            return self._clear_muse_memory()
        
        return None
    
    def _get_system_message(self):
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
    
    def _get_help_message(self):
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
    
    def _get_conversation_history(self):
        """Get the conversation history with the active muse."""
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
    
    def _clear_muse_memory(self):
        """Clear the memory of the active muse."""
        active_muse = get_current_muse()
        if not active_muse:
            return "No muse is currently active. Summon a muse first to clear memory."
        
        clear_muse_memory(active_muse.name)
        return f"Memory for {active_muse.name} has been cleared. All past conversations have been forgotten."


# Create a singleton instance for global use
muse_summoner = MuseSummoner()

def process_user_input(user_input):
    """
    Global function to process user input through the Muse Summoner system.
    This is the main entry point for external applications.
    """
    return muse_summoner.process_input(user_input)


# Test function for the memory-enhanced system
def test_memory_system():
    """Test the memory-enhanced Muse Summoner system with a series of interactions."""
    test_inputs = [
        "Come into fashion",
        "Help me reflect on my relationship with control.",
        "I feel like I'm always trying to control everything around me.",
        "What ritual might help me let go of control?",
        "That's beautiful. Can you write me a letter to my future self?",
        "Exit muse",
        "View history",
        "Come into fashion",
        "Do you remember our conversation about control?"
    ]
    
    print("=== Testing Memory-Enhanced Muse Summoner System ===\n")
    
    for i, test_input in enumerate(test_inputs, 1):
        print(f"Test {i}: \"{test_input}\"")
        response = process_user_input(test_input)
        print(f"Response:\n{response}\n")
        print("-" * 50)
    
    print("\n=== Test Complete ===")


# If this module is run directly, run the test
if __name__ == "__main__":
    test_memory_system()
