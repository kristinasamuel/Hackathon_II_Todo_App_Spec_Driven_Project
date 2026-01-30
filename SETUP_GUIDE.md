# Todo App Setup Guide

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd phase-3-Ai-Chatbot/backend
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Server
```bash
# Method 1: Using the provided run script (recommended)
python run_server.py

# Method 2: Direct uvicorn command
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

The backend will be available at: http://127.0.0.1:8000

## Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd phase-3-Ai-Chatbot/frontend_new
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Create Environment File
```bash
# Create .env.local file with:
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 4. Run the Application
```bash
npm run dev
```

The frontend will be available at: http://localhost:3000

## Default Credentials

After first run, a default admin user is automatically created:
- Email: admin@example.com
- Password: admin123

## API Endpoints

### Authentication
- POST /auth/login - User login
- POST /auth/signup - User registration
- GET /auth/me - Get current user

### Tasks
- GET /api/tasks - Get all tasks
- POST /api/tasks - Create task (201 Created)
- PUT /api/tasks/{id} - Update task
- PATCH /api/tasks/{id}/complete - Toggle completion
- DELETE /api/tasks/{id} - Delete task (204 No Content)

### Chat
- POST /api/chat - AI chatbot

### Health
- GET / - Health check
- GET /health - Health status

## Troubleshooting

1. If backend is not accessible, make sure it's running on 127.0.0.1:8000 (not 0.0.0.0:8000)
2. If authentication fails, use the default admin credentials or register a new user
3. Make sure the NEXT_PUBLIC_API_BASE_URL in frontend matches the backend URL
4. Rate limiting is active but shouldn't cause deployment issues