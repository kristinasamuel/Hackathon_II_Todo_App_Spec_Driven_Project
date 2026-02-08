# Task Manager Pro - Frontend

A modern, responsive task management application built with Next.js, TypeScript, and Tailwind CSS.

## Features

- User authentication (login/register)
- Task management (create, read, update, delete)
- Task completion toggle
- Responsive design for all device sizes
- JWT-based authentication
- Clean, professional UI

## Tech Stack

- Next.js 16+ with App Router
- React 18+
- TypeScript
- Tailwind CSS
- Axios for API requests
- JWT for authentication

## Getting Started

### Prerequisites

- Node.js 16+
- npm or yarn

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd frontend_new
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file in the root directory with the following content:
   ```
   NEXT_PUBLIC_API_BASE_URL=https://kristinasamuel-phase-3-ai-chatbot-todo-app.hf.space/
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) in your browser

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: The URL of the backend API server

## Available Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build the application for production
- `npm run start` - Start the production server
- `npm run lint` - Run ESLint

## Project Structure

```
src/
├── app/                 # Next.js App Router pages
│   ├── login/
│   │   └── page.tsx
│   ├── signup/
│   │   └── page.tsx
│   ├── dashboard/
│   │   └── page.tsx
│   ├── layout.tsx
│   └── page.tsx
├── components/          # Reusable UI components
│   ├── auth/
│   ├── tasks/
│   └── ui/
├── services/            # API and business logic
│   ├── api.ts
│   ├── auth.ts
│   └── tasks.ts
├── hooks/               # Custom React hooks
│   ├── useAuth.ts
│   └── useTasks.ts
└── utils/               # Utility functions
```

## API Integration

The frontend communicates with the backend API using the following endpoints:

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration

### Tasks
- `GET /api/{user_id}/tasks` - Get user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

## License

MIT
