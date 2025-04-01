"""
Fix for the trigger detection issue in the Muse Summoner system.
This update ensures proper handling of trigger phrases followed by tasks.
"""

import re
from muse_profiles import get_muse_by_trigger, get_all_muses

class TriggerDetector:
    def __init__(self):
        self.active_muse = None
        self.last_input = ""
    
    def detect_trigger(self, user_input):
        """
        Detect if the user input contains a trigger phrase for any muse.
        Returns the muse profile if a trigger is detected, None otherwise.
        """
        self.last_input = user_input
        
        # Get all muses and their trigger phrases
        all_muses = get_all_muses()
        
        # Check if any trigger phrase is in the user input
        for muse in all_muses:
            # Create a case-insensitive pattern for the trigger phrase
            pattern = re.compile(r'\b' + re.escape(muse.trigger_phrase) + r'\b', re.IGNORECASE)
            
            # Check if the pattern matches in the user input
            if pattern.search(user_input):
                self.active_muse = muse
                return muse
        
        return None
    
    def is_muse_active(self):
        """Check if a muse is currently active."""
        return self.active_muse is not None
    
    def get_active_muse(self):
        """Get the currently active muse."""
        return self.active_muse
    
    def deactivate_muse(self):
        """Deactivate the currently active muse."""
        self.active_muse = None
    
    def extract_task(self):
        """
        Extract the task from the user input after removing the trigger phrase.
        This helps isolate what the user is asking the muse to do.
        """
        if not self.active_muse or not self.last_input:
            return ""
        
        # Remove the trigger phrase from the input to get the task
        trigger = self.active_muse.trigger_phrase
        pattern = re.compile(r'\b' + re.escape(trigger) + r'\b', re.IGNORECASE)
        task = pattern.sub('', self.last_input).strip()
        
        # Remove any leading punctuation that might remain
        task = re.sub(r'^[.,;:\s]+', '', task)
        
        return task


# Create a singleton instance for global use
trigger_detector = TriggerDetector()

def detect_muse_trigger(user_input):
    """
    Global function to detect if a muse has been triggered in the user input.
    Returns the muse profile if triggered, None otherwise.
    """
    return trigger_detector.detect_trigger(user_input)

def get_current_muse():
    """Get the currently active muse."""
    return trigger_detector.get_active_muse()

def deactivate_current_muse():
    """Deactivate the currently active muse."""
    trigger_detector.deactivate_muse()

def extract_user_task():
    """Extract the task from the user input after removing the trigger phrase."""
    return trigger_detector.extract_task()
