# FastAPI Server

This project is a simple FastAPI server that provides a RESTful API and a WebSocket API.

## Project Structure

```
fastapi-server
├── app
│   ├── main.py          # Entry point of the FastAPI application
│   ├── api
│   │   ├── content.py   # Defines the /content GET endpoint
│   │   └── controls.py   # Defines the /controls WebSocket API endpoint
│   └── __init__.py      # Marks the app directory as a Python package
├── requirements.txt      # Lists the dependencies required for the project
└── README.md             # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd fastapi-server
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the FastAPI server, execute the following command:

```
uvicorn app.main:app --reload
```

You can access the API documentation at `http://127.0.0.1:8000/docs`.

### Endpoints

- **GET /content**: Returns the desired content.
- **WebSocket /controls**: Manages WebSocket connections and handles messages.