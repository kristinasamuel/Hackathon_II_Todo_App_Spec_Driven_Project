# Full Stack Todo Application

This is a complete full-stack todo application with both backend and frontend components.

## Project Structure

```
phase-2-fullstack-todo-app/
├── backend/          # FastAPI backend with authentication and task management
└── frontend_new/     # Next.js frontend with user interface
```

## Backend (FastAPI)

The backend is built with FastAPI and includes:

- User authentication (register/login)
- Task management (CRUD operations)
- JWT-based authentication
- Database integration (SQLModel)
- Rate limiting
- Security headers

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables (optional):
   ```bash
   # Copy .env.example to .env and modify as needed
   cp .env.example .env
   ```

4. Start the backend server:
   ```bash
   uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
   ```

## Frontend (Next.js)

The frontend is built with Next.js and includes:

- User authentication (login/signup)
- Task management interface
- Dashboard with task statistics
- Responsive design
- JWT-based session management

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend_new
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   # Create .env.local file
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

## Running the Full Application

1. Start the backend server (port 8000)
2. Start the frontend server (port 3000)
3. Access the application at http://localhost:3000

## Features

- User registration and authentication
- Create, read, update, and delete tasks
- Mark tasks as complete/incomplete
- View task statistics and charts
- Responsive UI for desktop and mobile
- Secure authentication with JWT tokens

## Technologies Used

- **Backend**: Python, FastAPI, SQLModel, PostgreSQL/SQLite
- **Frontend**: Next.js, React, TypeScript, Tailwind CSS
- **Authentication**: JWT tokens, bcrypt password hashing
- **Database**: SQLModel with SQLAlchemy ORM