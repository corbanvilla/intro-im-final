# Interactive Media Project

An interactive media experience that combines audio, imagery, and dynamic text visualization to tell the stories of students. This application presents audio recordings along with corresponding images and transcript text in an artistic, interactive interface that can be controlled through both on-screen interactions and physical Arduino controls.

## Project Overview

This project consists of three main components:

1. **Client**: A browser-based application built with p5.js that handles the visualization, audio playback, and user interaction.
2. **Server**: A FastAPI backend that serves content and manages WebSocket connections for real-time control, while also integrating with Arduino via serial.
3. **Transcription**: Python scripts for processing and annotating audio transcript data.

## Project Structure

```
final/
├── client/                 # Browser-based frontend application
│   ├── index.html          # Main HTML entry point
│   ├── assets/             # Media assets (audio, images, fonts, transcripts)
│   │   ├── audio/          # Audio recordings of speakers
│   │   ├── fonts/          # Inter font files in various weights
│   │   ├── images/         # Images of speakers/subjects
│   │   └── transcripts/    # JSON transcript files with timing information
│   ├── code/               # Client-side JavaScript
│   │   ├── audio.js        # Audio handling functionality
│   │   ├── content.js      # Content loading and management
│   │   ├── controls.js     # UI and physical controls management
│   │   ├── image.js        # Image rendering
│   │   ├── sketch.js       # Main p5.js sketch with core application logic
│   │   ├── style.css       # CSS styling
│   │   └── textboxes.js    # Dynamic text visualization
│   └── libraries/          # External libraries (p5.js, p5.sound)
│
├── server/                 # FastAPI backend server
│   ├── app/                # Server application code
│   │   ├── database.py     # Database operations and state management
│   │   ├── main.py         # FastAPI app entry point
│   │   ├── api/            # API endpoints
│   │   │   ├── content.py  # Content delivery endpoint
│   │   │   └── controls.py # WebSocket endpoint for controls
│   │   └── ardunio/        # Arduino integration
│   │       ├── arduino.c   # Arduino code
│   │       ├── serial_read.py  # Serial communication with Arduino
│   │       └── requirements.txt # Dependencies for Arduino integration
│   ├── README.md           # Server-specific documentation
│   ├── requirements.txt    # Python dependencies for server
│   └── start.sh            # Server startup script
│
└── transcribe/             # Transcription processing utilities
    ├── annotate_transcriptions.py  # Script to annotate transcriptions
    ├── transcribe.py       # Script to generate transcriptions
    ├── requirements.txt    # Python dependencies for transcription
    └── sources/            # Source text files for transcriptions
```

## Setup Instructions

### Prerequisites
- Python 3.10+ 
- Arduino IDE (for hardware controller)

### Server Setup

1. Navigate to the server directory:
   ```
   cd server
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
   - On Windows:
     ```
     venv\Scripts\activate
     ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Start the server:
   ```
   ./start.sh
   ```
   or
   ```
   uvicorn app.main:app --reload
   ```

### Arduino Setup (Optional)

1. Connect your Arduino board
2. Upload the arduino.c code using the Arduino IDE
3. Note the serial port your Arduino is connected to
4. Update the serial port in server/app/ardunio/serial_read.py if needed

### Client Access

Once the server is running, open a web browser and navigate to:
```
http://localhost:8000
```

## Usage

- **Click anywhere** on the screen to start the experience
- **Flip the red switch** on the Arduino to pause/resume playback
- **Rotate potentiometer 2** to adjust volume
- **Rotate potentiometer 3** to adjust playback speed
- **Press buttons 1 or 2** to trigger a transition to the next content

## Transcription Tools

The project includes tools for processing audio transcriptions:

1. Navigate to the transcribe directory:
   ```
   cd transcribe
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Use transcribe.py to generate new transcriptions
