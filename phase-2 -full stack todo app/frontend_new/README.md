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
   NEXT_PUBLIC_API_BASE_URL=https://kristinasamuel-todo-app-deploy.hf.space
   ```

   For local development with a local backend, use:
   ```
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) in your browser

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: The URL of the backend API server (for production: `https://kristinasamuel-todo-app-deploy.hf.space`, for local development: `http://localhost:8000`)

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

### Manual Deployment Steps:

1. Fork or clone this repository
2. Create a new project on Vercel
3. Import your repository
4. Set the following environment variable in Vercel dashboard:
   - `NEXT_PUBLIC_API_BASE_URL`: URL of your deployed backend API
5. Click Deploy

### Build Locally

To build the application locally, run:

```bash
npm run build
```

The build output will be in the `out` directory if using static export, or you can run it with `npm start`.

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
