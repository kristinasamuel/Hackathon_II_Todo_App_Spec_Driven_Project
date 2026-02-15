# Todo Backend API

Backend API for the Full-Stack Todo Application

## Getting Started

1. Navigate to the backend directory:
   ```bash
   cd phase-3-Ai-Chatbot/backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

   Or alternatively, run directly with Python:
   ```bash
   python main.py
   ```

The API will be available at http://127.0.0.1:8000

## Endpoints

- `GET /` - Health check
- `GET /health` - Health status
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `POST /api/chat` - Chat with AI assistant