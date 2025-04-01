"""
Muse Summoner System - Conversation Storage Module

This module handles the storage and retrieval of conversation history.
It integrates with the memory system to provide persistent storage of user-muse interactions.
"""

import os
import json
import datetime
from memory_system import add_conversation_memory, get_conversation_history, get_memory_context

class ConversationManager:
    def __init__(self):
        """Initialize the conversation manager."""
        self.current_conversation = []
        self.active_muse_name = None
    
    def start_conversation(self, muse_name):
        """
        Start a new conversation with a muse.
        
        Args:
            muse_name (str): The name of the muse
        """
        self.active_muse_name = muse_name
        self.current_conversation = []
    
    def add_interaction(self, user_input, muse_response):
        """
        Add a user-muse interaction to the current conversation and store it in memory.
        
        Args:
            user_input (str): The user's input
            muse_response (str): The muse's response
        """
        if not self.active_muse_name:
            return
        
        # Add to current conversation
        interaction = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_input": user_input,
            "muse_response": muse_response
        }
        self.current_conversation.append(interaction)
        
        # Store in persistent memory
        add_conversation_memory(self.active_muse_name, user_input, muse_response)
    
    def end_conversation(self):
        """End the current conversation."""
        self.active_muse_name = None
        self.current_conversation = []
    
    def get_current_conversation_summary(self):
        """
        Get a summary of the current conversation.
        
        Returns:
            str: A summary of the current conversation
        """
        if not self.current_conversation:
            return "No current conversation."
        
        summary = "Current conversation:\n\n"
        
        for i, interaction in enumerate(self.current_conversation[-3:], 1):
            timestamp = datetime.datetime.fromisoformat(interaction["timestamp"])
            formatted_time = timestamp.strftime("%H:%M:%S")
            
            summary += f"Interaction {i} ({formatted_time}):\n"
            summary += f"User: {interaction['user_input']}\n"
            summary += f"Muse: {interaction['muse_response'][:100]}...\n\n"
        
        return summary
    
    def get_conversation_context(self, current_input):
        """
        Get context from the current conversation and memory for generating a response.
        
        Args:
            current_input (str): The current user input
            
        Returns:
            dict: A dictionary containing conversation context
        """
        if not self.active_muse_name:
            return {"current_conversation": [], "memory_context": {}}
        
        # Get memory context
        memory_context = get_memory_context(self.active_muse_name, current_input)
        
        return {
            "current_conversation": self.current_conversation[-3:],
            "memory_context": memory_context
        }
    
    def is_conversation_active(self):
        """
        Check if a conversation is currently active.
        
        Returns:
            bool: True if a conversation is active, False otherwise
        """
        return self.active_muse_name is not None
    
    def get_active_muse_name(self):
        """
        Get the name of the currently active muse.
        
        Returns:
            str: The name of the active muse, or None if no conversation is active
        """
        return self.active_muse_name


# Create a singleton instance for global use
conversation_manager = ConversationManager()

def start_muse_conversation(muse_name):
    """
    Global function to start a conversation with a muse.
    
    Args:
        muse_name (str): The name of the muse
    """
    conversation_manager.start_conversation(muse_name)

def add_conversation_interaction(user_input, muse_response):
    """
    Global function to add a user-muse interaction to the current conversation.
    
    Args:
        user_input (str): The user's input
        muse_response (str): The muse's response
    """
    conversation_manager.add_interaction(user_input, muse_response)

def end_muse_conversation():
    """Global function to end the current conversation."""
    conversation_manager.end_conversation()

def get_conversation_context(current_input):
    """
    Global function to get context from the current conversation and memory.
    
    Args:
        current_input (str): The current user input
        
    Returns:
        dict: A dictionary containing conversation context
    """
    return conversation_manager.get_conversation_context(current_input)

def is_muse_conversation_active():
    """
    Global function to check if a conversation is currently active.
    
    Returns:
        bool: True if a conversation is active, False otherwise
    """
    return conversation_manager.is_conversation_active()

def get_active_muse():
    """
    Global function to get the name of the currently active muse.
    
    Returns:
        str: The name of the active muse, or None if no conversation is active
    """
    return conversation_manager.get_active_muse_name()
