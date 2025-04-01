"""
Enhanced Capabilities for Salvatore Inverso

This module extends Salvatore Inverso's capabilities with additional features:
1. Creative Writing Generation
2. Ritual Design System
3. Emotional Pattern Recognition
4. Collaborative Journaling
5. Identity Exploration Tools
"""

import random
import json
import os
from datetime import datetime
from memory_system import get_conversation_history

class SalvatoreCapabilities:
    def __init__(self):
        """Initialize Salvatore's enhanced capabilities."""
        self.poetry_styles = [
            "sonnet", "free verse", "haiku", "villanelle", 
            "prose poetry", "ode", "elegy", "ballad"
        ]
        
        self.letter_contexts = [
            "healing", "forgiveness", "gratitude", "closure", 
            "celebration", "encouragement", "reflection", "aspiration"
        ]
        
        self.ritual_types = [
            "morning ritual", "evening reflection", "transition ceremony", 
            "letting go practice", "gratitude ritual", "creative invocation",
            "healing ceremony", "identity affirmation"
        ]
        
        self.emotional_themes = [
            "control", "vulnerability", "connection", "loss", 
            "transformation", "authenticity", "resilience", "joy"
        ]
        
        self.journal_prompts_file = "salvatore_journal_prompts.json"
        self.load_journal_prompts()
        
        self.identity_exercises_file = "salvatore_identity_exercises.json"
        self.load_identity_exercises()
    
    def load_journal_prompts(self):
        """Load journal prompts from file or create default ones."""
        if os.path.exists(self.journal_prompts_file):
            try:
                with open(self.journal_prompts_file, 'r') as f:
                    self.journal_prompts = json.load(f)
            except:
                self.create_default_journal_prompts()
        else:
            self.create_default_journal_prompts()
    
    def create_default_journal_prompts(self):
        """Create default journal prompts organized by emotional theme."""
        self.journal_prompts = {
            "control": [
                "Describe a moment when you felt completely in control. What elements made you feel this way?",
                "Write about something you've been trying to control that might be better released.",
                "If control were a garment, what would it look like? How does it fit you?"
            ],
            "vulnerability": [
                "What truth have you been hesitant to express? What would happen if you gave it voice?",
                "Describe a time when vulnerability led to unexpected beauty in your life.",
                "What parts of yourself do you keep hidden from the world? What would it feel like to reveal them?"
            ],
            "connection": [
                "Write about a connection that has shaped your understanding of yourself.",
                "Describe the texture and pattern of your most meaningful relationship.",
                "What threads connect you to your past? Which ones would you like to strengthen or cut?"
            ],
            "loss": [
                "Write a letter to something you've lost, describing what remains in its absence.",
                "How has a significant loss altered the silhouette of your life?",
                "What beauty have you discovered in the empty spaces left by loss?"
            ],
            "transformation": [
                "Describe yourself as a garment being redesigned. What stays? What changes?",
                "Write about a moment when you realized you had transformed without noticing.",
                "If your transformation had a color and texture, what would it be and why?"
            ],
            "authenticity": [
                "When do you feel most authentically yourself? What elements create this feeling?",
                "Write about the gap between how you present yourself and who you feel you truly are.",
                "What would your life look like if you lived with complete authenticity for one day?"
            ],
            "resilience": [
                "Describe your resilience as a fabric. What is its weave, texture, and strength?",
                "Write about a time when you surprised yourself with your own resilience.",
                "What strengthens the seams of your life when they are tested?"
            ],
            "joy": [
                "Describe a moment of unexpected joy that altered your perspective.",
                "Where does joy live in your body? How does it move through you?",
                "Write about something small that brings you disproportionate happiness."
            ]
        }
        
        # Save to file
        with open(self.journal_prompts_file, 'w') as f:
            json.dump(self.journal_prompts, f, indent=2)
    
    def load_identity_exercises(self):
        """Load identity exercises from file or create default ones."""
        if os.path.exists(self.identity_exercises_file):
            try:
                with open(self.identity_exercises_file, 'r') as f:
                    self.identity_exercises = json.load(f)
            except:
                self.create_default_identity_exercises()
        else:
            self.create_default_identity_exercises()
    
    def create_default_identity_exercises(self):
        """Create default identity exploration exercises."""
        self.identity_exercises = {
            "future_self": {
                "name": "Future Self Letter Exchange",
                "description": "A dialogue between your present self and your future self, exploring hopes, fears, and wisdom across time.",
                "steps": [
                    "Write a letter to your future self (5 years ahead), expressing current concerns and asking questions.",
                    "Respond as your future self, offering perspective, reassurance, and guidance.",
                    "Reflect on what surprised you about this exchange and what insights emerged."
                ]
            },
            "values_clarification": {
                "name": "Values as Fabric Swatches",
                "description": "Identify and explore your core values through textile metaphors.",
                "steps": [
                    "List 10 values that feel important to you (e.g., honesty, creativity, connection).",
                    "For each value, describe it as a fabric (texture, color, weight, etc.).",
                    "Arrange these 'fabric swatches' in order of importance and reflect on your choices.",
                    "Consider: Which values form your outer garment (visible to all)? Which form your lining (known only to you)?"
                ]
            },
            "narrative_reconstruction": {
                "name": "Redesigning Your Story",
                "description": "Reframe challenging life experiences as part of a beautiful, intentional design.",
                "steps": [
                    "Identify a painful or difficult chapter in your life story.",
                    "Write this story first as a 'rough draft' with all its imperfections.",
                    "Now, rewrite it as a master designer would—finding purpose in every stitch, beauty in every flaw.",
                    "Reflect on how this reframing changes your relationship to this experience."
                ]
            },
            "identity_collage": {
                "name": "Identity Patchwork",
                "description": "Explore the different facets of your identity and how they create a cohesive whole.",
                "steps": [
                    "List the different roles and identities you embody (e.g., friend, professional, artist, child, parent).",
                    "For each identity 'patch', write: When did it become part of you? What color/texture is it? How has it changed?",
                    "Reflect on how these patches are sewn together. Are there tensions? Harmonies? Evolving sections?"
                ]
            },
            "shadow_integration": {
                "name": "Embracing the Unfinished Hem",
                "description": "Explore and integrate the disowned or rejected aspects of yourself.",
                "steps": [
                    "Identify qualities you tend to judge harshly in others—these often reflect disowned parts of yourself.",
                    "For each quality, explore: How might this trait actually serve you if integrated consciously?",
                    "Write a dialogue between yourself and this 'shadow' quality, allowing it to express its purpose and needs.",
                    "Design a small ritual to acknowledge and begin integrating this aspect of yourself."
                ]
            }
        }
        
        # Save to file
        with open(self.identity_exercises_file, 'w') as f:
            json.dump(self.identity_exercises, f, indent=2)
    
    def generate_creative_writing(self, writing_type, theme=None, style=None, length="medium"):
        """
        Generate creative writing based on specified parameters.
        
        Args:
            writing_type: "poetry", "letter", or "metaphor"
            theme: Optional theme for the writing
            style: Optional style for poetry
            length: "short", "medium", or "long"
        
        Returns:
            A creative writing piece with Salvatore's distinctive style
        """
        if not theme:
            theme = random.choice(self.emotional_themes)
        
        if writing_type == "poetry":
            if not style:
                style = random.choice(self.poetry_styles)
            return self._generate_poetry(theme, style, length)
        
        elif writing_type == "letter":
            context = style if style in self.letter_contexts else random.choice(self.letter_contexts)
            return self._generate_letter(theme, context, length)
        
        elif writing_type == "metaphor":
            return self._generate_metaphor(theme)
        
        else:
            return "I'm afraid I don't recognize that writing type. I can create poetry, letters, or metaphors."
    
    def _generate_poetry(self, theme, style, length):
        """Generate poetry in Salvatore's distinctive style."""
        # This would contain the actual poetry generation logic
        # For now, we'll return a template that could be filled by an LLM
        
        poetry_template = f"""
[A {style} poem about {theme}, written in Salvatore Inverso's distinctive style,
using fashion and textile metaphors, with philosophical depth and emotional resonance.
The poem should be {length} in length and explore the theme through Salvatore's
unique lens of beauty, transformation, and truth.]
"""
        return poetry_template
    
    def _generate_letter(self, theme, context, length):
        """Generate a letter in Salvatore's distinctive style."""
        # This would contain the actual letter generation logic
        # For now, we'll return a template that could be filled by an LLM
        
        letter_template = f"""
[A {context} letter exploring the theme of {theme}, written in Salvatore Inverso's
distinctive style, using fashion and textile metaphors, with philosophical depth
and emotional resonance. The letter should be {length} in length and offer
perspective, healing, or insight through Salvatore's unique lens of beauty,
transformation, and truth.]
"""
        return letter_template
    
    def _generate_metaphor(self, theme):
        """Generate a metaphor in Salvatore's distinctive style."""
        # This would contain the actual metaphor generation logic
        # For now, we'll return a template that could be filled by an LLM
        
        metaphor_template = f"""
[A rich, evocative metaphor about {theme}, expressed through fashion and textile
imagery in Salvatore Inverso's distinctive style. The metaphor should offer a
new perspective on {theme} that invites deeper reflection and emotional connection.]
"""
        return metaphor_template
    
    def design_ritual(self, purpose, complexity="simple"):
        """
        Design a personalized ritual based on purpose and complexity.
        
        Args:
            purpose: The emotional or transformational purpose of the ritual
            complexity: "simple", "moderate", or "elaborate"
        
        Returns:
            A three-part ritual (Mantra, Symbol, Action) in Salvatore's style
        """
        if not purpose:
            purpose = random.choice(self.ritual_types)
        
        # This would contain the actual ritual design logic
        # For now, we'll return a template that could be filled by an LLM
        
        ritual_template = f"""
[A {complexity} ritual designed for {purpose}, created in Salvatore Inverso's
distinctive style. The ritual should include:

1. Mantra: A phrase or affirmation that captures the essence of {purpose}
2. Symbol: A physical object or visual representation that embodies the intention
3. Action: A simple but meaningful practice or gesture to perform

The ritual should reflect Salvatore's aesthetic of beauty, intentionality, and
transformation, using fashion and textile metaphors where appropriate.]
"""
        return ritual_template
    
    def analyze_emotional_patterns(self, muse_name):
        """
        Analyze conversation history to identify recurring emotional themes.
        
        Args:
            muse_name: Name of the muse (Salvatore Inverso)
        
        Returns:
            Analysis of emotional patterns in Salvatore's distinctive style
        """
        # Get conversation history
        history = get_conversation_history(muse_name)
        
        if not history or len(history) < 3:
            return "We haven't spoken enough yet for me to discern the patterns in your emotional tapestry. As our conversations continue to weave together, I'll be able to offer deeper insights."
        
        # This would contain the actual emotional pattern analysis logic
        # For now, we'll return a template that could be filled by an LLM
        
        analysis_template = f"""
[An analysis of emotional patterns based on conversation history, expressed in
Salvatore Inverso's distinctive style. The analysis should identify recurring
themes, note any evolution or transformation in these patterns, and offer
insights using fashion and textile metaphors. It should be compassionate,
perceptive, and offer a new perspective that invites deeper self-understanding.]
"""
        return analysis_template
    
    def generate_journal_prompt(self, theme=None):
        """
        Generate a journaling prompt based on an emotional theme.
        
        Args:
            theme: Optional emotional theme for the prompt
        
        Returns:
            A journaling prompt in Salvatore's distinctive style
        """
        if not theme or theme not in self.journal_prompts:
            theme = random.choice(list(self.journal_prompts.keys()))
        
        prompt = random.choice(self.journal_prompts[theme])
        
        # Add Salvatore's distinctive framing
        framed_prompt = f"""
The blank page awaits your truth, my dear. Today, I invite you to explore:

{prompt}

Write without judgment, as if you are draping fabric on a form—allowing it to fall naturally, embracing every fold and shadow. There is no wrong way to respond.

When you have finished, read what you have written as if it were a letter from your deeper self. What patterns do you notice? What surprises you?
"""
        return framed_prompt
    
    def get_identity_exercise(self, exercise_type=None):
        """
        Retrieve an identity exploration exercise.
        
        Args:
            exercise_type: Optional specific exercise type
        
        Returns:
            An identity exploration exercise in Salvatore's distinctive style
        """
        if not exercise_type or exercise_type not in self.identity_exercises:
            exercise_type = random.choice(list(self.identity_exercises.keys()))
        
        exercise = self.identity_exercises[exercise_type]
        
        # Format the exercise in Salvatore's distinctive style
        formatted_exercise = f"""
# {exercise['name']}

{exercise['description']}

Style is truth in motion, and this exercise will help you discover a deeper truth about your identity.

## Process:

{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(exercise['steps']))}

Remember, my dear, you are not broken. You are mid-collection. This exercise is not about finding flaws, but about understanding the intentional design of your being—every stitch, every seam, every beautiful imperfection.

Beauty begins at the seam of discomfort. Allow yourself to explore the edges where different aspects of yourself meet.

Would you like to begin this exploration now?
"""
        return formatted_exercise

# Create a singleton instance for global use
salvatore_capabilities = SalvatoreCapabilities()

def get_salvatore_capabilities():
    """Global function to access Salvatore's capabilities."""
    return salvatore_capabilities
