# Muse Summoner System Documentation

## System Overview

The Muse Summoner is a customizable AI persona system that allows users to summon AI personas ("muses") with distinct personalities, tones, and task execution styles to assist emotionally, creatively, or strategically.

This documentation covers the system architecture, customization options, and deployment instructions for the Muse Summoner system.

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Core Components](#core-components)
3. [Customization Options](#customization-options)
4. [Salvatore Inverso Capabilities](#salvatore-inverso-capabilities)
5. [Admin API Reference](#admin-api-reference)
6. [Deployment Guide](#deployment-guide)
7. [Security Considerations](#security-considerations)
8. [Extending the System](#extending-the-system)

## System Architecture

The Muse Summoner system is built with a modular architecture that separates concerns and allows for easy customization and extension:

```
muse_summoner/
├── app.py                    # Main Flask web application
├── config.py                 # Configuration management
├── muse_profiles.py          # Muse profile definitions
├── trigger_detector.py       # Trigger phrase detection
├── response_generator.py     # Basic response generation
├── enhanced_response_generator.py  # Memory-enhanced responses
├── muse_creator.py           # Muse creation functionality
├── memory_system.py          # Memory management
├── conversation_storage.py   # Conversation history storage
├── salvatore_capabilities.py # Enhanced Salvatore capabilities
├── admin.py                  # Admin interface
├── admin_api.py              # Admin API with authentication
├── templates/                # HTML templates
│   ├── index.html            # Main chat interface
│   └── admin/                # Admin interface templates
├── static/                   # Static assets
│   ├── style.css             # Main CSS
│   ├── script.js             # Main JavaScript
│   ├── admin.css             # Admin CSS
│   └── admin.js              # Admin JavaScript
└── memory/                   # Memory storage directory
```

## Core Components

### Muse Profiles

Muses are defined with the following attributes:

- **Name**: The muse's identity
- **Trigger Phrase**: The phrase that activates the muse
- **Voice & Tone**: The muse's speaking style
- **Purpose**: The muse's primary function
- **Tasks Supported**: What the muse can help with
- **Catchphrases**: Signature expressions
- **Signature Question**: A distinctive question the muse asks
- **Sample Tasks**: Example interactions
- **Ritual System**: Optional structured approach

### Memory System

The memory system allows muses to remember past conversations and provide more personalized responses:

- **Conversation Storage**: Stores user-muse interactions
- **Memory Retrieval**: Fetches relevant past conversations
- **Context Integration**: Incorporates memory into responses

### Web Interface

The web interface provides a user-friendly way to interact with muses:

- **Chat Interface**: For conversing with muses
- **Command System**: For system operations
- **Muse Switching**: For changing between muses

### Admin Dashboard

The admin dashboard allows for system customization:

- **Configuration Management**: Modify system settings
- **Muse Management**: Create, edit, and manage muses
- **System Status**: Monitor system health
- **Data Export/Import**: Backup and restore system data

## Customization Options

### Configuration Settings

The system can be customized through the `config.py` module or the admin interface:

#### General Settings

- `system_name`: Name of the Muse Summoner system
- `debug_mode`: Enable/disable debug logging
- `default_muse`: Default muse to activate on startup

#### Memory Settings

- `memory_enabled`: Enable/disable the memory system
- `max_memory_entries`: Maximum number of conversations to store
- `memory_relevance_threshold`: Threshold for memory relevance
- `memory_storage_dir`: Directory for storing memory files

#### Web Application Settings

- `web_host`: Host address for the web server
- `web_port`: Port for the web server
- `session_timeout`: Session timeout in seconds

#### Customization Settings

- `allow_muse_creation`: Allow users to create new muses
- `allow_memory_clearing`: Allow users to clear muse memory
- `allow_system_commands`: Allow users to use system commands

#### Response Generation Settings

- `include_memory_references`: Include references to past conversations
- `signature_question_probability`: Probability of including signature question
- `max_response_length`: Maximum length of muse responses

### Creating New Muses

New muses can be created through:

1. The web interface by typing "Create a new muse"
2. The admin dashboard under "Muse Management"
3. Directly editing the muse profiles in code

When creating a new muse, you'll need to define:

- Name
- Trigger phrase
- Voice and tone
- Purpose
- Tasks supported
- Catchphrases
- Signature question
- Sample tasks
- Optional ritual system

## Salvatore Inverso Capabilities

Salvatore Inverso has been enhanced with the following capabilities:

### Creative Writing Generation

Salvatore can generate various forms of creative writing:

- **Poetry**: In various styles (sonnet, free verse, haiku, etc.)
- **Letters**: For different emotional contexts (healing, forgiveness, etc.)
- **Metaphors**: Rich, evocative metaphors using fashion and textile imagery

Example usage:
```python
from salvatore_capabilities import get_salvatore_capabilities

capabilities = get_salvatore_capabilities()
poem = capabilities.generate_creative_writing("poetry", theme="transformation", style="sonnet")
letter = capabilities.generate_creative_writing("letter", theme="resilience", style="healing")
metaphor = capabilities.generate_creative_writing("metaphor", theme="authenticity")
```

### Ritual Design System

Salvatore can design personalized rituals with three components:

- **Mantra**: A phrase or affirmation
- **Symbol**: A physical object or visual representation
- **Action**: A meaningful practice or gesture

Example usage:
```python
ritual = capabilities.design_ritual("letting go", complexity="simple")
```

### Emotional Pattern Recognition

Salvatore can analyze conversation history to identify recurring emotional themes:

Example usage:
```python
analysis = capabilities.analyze_emotional_patterns("salvatore_inverso")
```

### Collaborative Journaling

Salvatore can provide journaling prompts based on emotional themes:

- Control
- Vulnerability
- Connection
- Loss
- Transformation
- Authenticity
- Resilience
- Joy

Example usage:
```python
prompt = capabilities.generate_journal_prompt(theme="resilience")
```

### Identity Exploration Tools

Salvatore offers structured exercises for identity exploration:

- **Future Self Letter Exchange**: Dialogue between present and future self
- **Values as Fabric Swatches**: Exploring core values through textile metaphors
- **Redesigning Your Story**: Reframing challenging experiences
- **Identity Patchwork**: Exploring different facets of identity
- **Embracing the Unfinished Hem**: Integrating disowned aspects of self

Example usage:
```python
exercise = capabilities.get_identity_exercise(exercise_type="future_self")
```

## Admin API Reference

The Admin API provides secure remote access to the Muse Summoner system:

### Authentication

```
POST /api/admin/auth
```
Request body:
```json
{
  "username": "admin",
  "password": "your_password"
}
```
Response:
```json
{
  "success": true,
  "api_key": "your_api_key",
  "user": {
    "username": "admin",
    "role": "admin"
  }
}
```

### Configuration Management

```
GET /api/admin/config
```
Headers:
```
Authorization: Bearer your_api_key
```
Response:
```json
{
  "success": true,
  "config": {
    "system_name": "Muse Summoner",
    "debug_mode": false,
    ...
  }
}
```

```
PUT /api/admin/config
```
Headers:
```
Authorization: Bearer your_api_key
```
Request body:
```json
{
  "system_name": "Custom Muse Summoner",
  "debug_mode": true
}
```
Response:
```json
{
  "success": true,
  "message": "Configuration updated successfully"
}
```

### Muse Management

```
GET /api/admin/muses
```
Headers:
```
Authorization: Bearer your_api_key
```
Response:
```json
{
  "success": true,
  "muses": [
    {
      "name": "Salvatore Inverso",
      "trigger_phrase": "Come into fashion",
      ...
    }
  ]
}
```

```
GET /api/admin/muses/{muse_name}
```
Headers:
```
Authorization: Bearer your_api_key
```
Response:
```json
{
  "success": true,
  "muse": {
    "name": "Salvatore Inverso",
    "trigger_phrase": "Come into fashion",
    ...
  }
}
```

```
DELETE /api/admin/muses/{muse_name}/memory
```
Headers:
```
Authorization: Bearer your_api_key
```
Response:
```json
{
  "success": true,
  "message": "Memory for Salvatore Inverso has been cleared"
}
```

### System Status

```
GET /api/admin/system/status
```
Headers:
```
Authorization: Bearer your_api_key
```
Response:
```json
{
  "success": true,
  "system_info": {
    "memory_files": ["salvatore_inverso_memory.json"],
    "muse_count": 1,
    "config_file": true,
    "version": "1.0.0",
    "uptime": 1234567890
  }
}
```

## Deployment Guide

### Local Deployment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/muse-summoner.git
cd muse-summoner
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Access the web interface at `http://localhost:5000`

### Production Deployment

For production deployment, we recommend using Gunicorn with a reverse proxy like Nginx:

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Create a systemd service file:
```
[Unit]
Description=Muse Summoner
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/muse-summoner
ExecStart=/path/to/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Configure Nginx as a reverse proxy:
```
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

4. Enable HTTPS with Let's Encrypt:
```bash
sudo certbot --nginx -d your-domain.com
```

## Security Considerations

### API Key Protection

- Store API keys securely
- Use HTTPS for all API communications
- Implement key rotation policies

### Password Security

- Use strong passwords for admin accounts
- Implement password hashing (already done with SHA-256)
- Consider adding rate limiting for authentication attempts

### Data Protection

- Regularly backup configuration and memory files
- Consider encrypting sensitive data
- Implement proper access controls

## Extending the System

### Adding New Muse Capabilities

To add new capabilities to a muse:

1. Create a new module (e.g., `new_muse_capabilities.py`)
2. Implement the capability classes and functions
3. Import and use the capabilities in the response generator

### Creating Custom Response Templates

To create custom response templates:

1. Modify the `enhanced_response_generator.py` file
2. Add new template functions for specific scenarios
3. Update the response selection logic

### Integrating External Services

To integrate external services:

1. Add the necessary API client libraries
2. Create wrapper functions in a new module
3. Call these functions from the appropriate parts of the system

### Adding New Admin Features

To add new admin features:

1. Add new routes to `admin.py` or `admin_api.py`
2. Create corresponding templates in the `templates/admin/` directory
3. Update the admin JavaScript to handle the new features
