# Muse Summoner

A customizable AI persona system that allows users to summon AI personas ("muses") with distinct personalities, tones, and task execution styles to assist emotionally, creatively, or strategically.

## Features

- **Multiple Muse Personas**: Create and interact with AI personas that have unique voices, tones, and purposes
- **Trigger Phrase Detection**: Summon muses using their unique trigger phrases
- **Persistent Memory**: Muses remember past conversations and provide personalized responses
- **Web Interface**: User-friendly web application for interacting with muses
- **Admin Dashboard**: Comprehensive admin interface for system customization
- **Extensible Architecture**: Easily add new muses and capabilities

## Getting Started

### Prerequisites

- Python 3.10+
- Flask
- Git (for version control)

### Installation

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

## Usage

### Summoning a Muse

To interact with a muse, use their trigger phrase. For example, to summon Salvatore Inverso:

```
Come into fashion
```

### Available Commands

- `List muses` - Shows all available muses
- `Create a new muse` - Starts the process of creating a custom muse
- `Exit muse` - Exits the currently active muse
- `View history` - Shows your recent conversation history with the active muse
- `Clear memory` - Clears the memory of the active muse
- `Help` - Shows the help message with available commands

### Admin Interface

Access the admin interface at `http://localhost:5000/admin` to:

- Modify system configuration
- Manage muses
- View system status
- Export/import system data

## Customization

### Creating New Muses

You can create new muses with unique personalities through:

1. The web interface by typing "Create a new muse"
2. The admin dashboard under "Muse Management"
3. Directly editing the muse profiles in code

### Configuration Options

The system can be customized through the `config.py` file or the admin interface. Key configuration options include:

- Memory settings (storage, relevance threshold)
- Web application settings (host, port)
- Customization permissions
- Response generation parameters

## Deployment

### Local Deployment

For local deployment, simply run:

```bash
python app.py
```

### Production Deployment

For production deployment:

1. Set up a virtual environment
2. Install Gunicorn:
```bash
pip install gunicorn
```

3. Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Created for enhancing human-AI interaction through personalized experiences
- Inspired by the concept of creative muses throughout history
