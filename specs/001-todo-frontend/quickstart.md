# Quickstart Guide: Phase II Frontend - Todo Full-Stack Web Application

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Access to the backend API (running on localhost:8000 by default)
- Git for version control

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
cd "D:\hackathon_2_Ai_todo_app\Hackathon_II_Todo_Spec_Driven_project\phase-2 -full stack todo app"
```

### 2. Create Frontend Directory
```bash
mkdir frontend
cd frontend
```

### 3. Initialize Next.js Project
```bash
npm create next-app@latest .
# Select options:
# - Yes for TypeScript
# - Yes for ESLint
# - Yes for Tailwind CSS
# - No for App Router (use existing structure)
# - No for Src directory
# - Yes for Import alias (@/*)
```

### 4. Install Additional Dependencies
```bash
npm install @types/node @types/react @types/react-dom
npm install axios react-icons
```

### 5. Configure Environment Variables
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### 6. Start Development Server
```bash
npm run dev
```

Your frontend should now be running on http://localhost:3000

## Project Structure Overview

```
frontend/
├── src/
│   ├── app/                # Next.js App Router pages
│   │   ├── layout.tsx      # Root layout
│   │   ├── page.tsx        # Home page
│   │   ├── login/page.tsx  # Login page
│   │   ├── signup/page.tsx # Signup page
│   │   └── dashboard/page.tsx # Dashboard page
│   ├── components/         # Reusable UI components
│   │   ├── auth/          # Authentication components
│   │   ├── tasks/         # Task management components
│   │   └── ui/            # Generic UI components
│   ├── services/          # API and business logic
│   │   ├── api.ts         # API service
│   │   ├── auth.ts        # Authentication service
│   │   └── tasks.ts       # Task service
│   ├── hooks/             # Custom React hooks
│   │   ├── useAuth.ts     # Authentication hook
│   │   └── useTasks.ts    # Task management hook
│   ├── utils/             # Utility functions
│   │   ├── jwt.ts         # JWT utilities
│   │   └── constants.ts   # Constants
│   └── styles/            # Styling
│       └── globals.css    # Global styles
├── public/                # Static assets
├── package.json          # Dependencies and scripts
├── next.config.js        # Next.js configuration
├── tailwind.config.js    # Tailwind CSS configuration
└── tsconfig.json         # TypeScript configuration
```

## Key Configuration Files

### Next.js Configuration (next.config.js)
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  },
}

module.exports = nextConfig
```

### Tailwind CSS Configuration (tailwind.config.js)
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
    },
  },
  plugins: [],
}
```

## API Integration

The frontend communicates with the backend API located at:
- Base URL: `http://localhost:8000` (or as configured in environment variables)
- Authentication endpoints: `/auth/*`
- Task endpoints: `/api/{user_id}/tasks`

All authenticated requests must include the JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Authentication Flow

1. User visits `/login` or `/signup` page
2. Credentials are sent to backend authentication endpoint
3. JWT token is received and stored in browser storage
4. Token is included in all subsequent API requests
5. Token expiration is monitored and refresh is handled automatically

## Running Tests

### Unit Tests
```bash
npm run test
```

### Linting
```bash
npm run lint
```

### Building for Production
```bash
npm run build
npm start
```

## Common Commands

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter
- `npm run test` - Run tests
- `npm run test:watch` - Run tests in watch mode

## Troubleshooting

### Backend Connection Issues
- Ensure the backend server is running on the configured port
- Check that CORS is properly configured on the backend
- Verify the API URL in environment variables

### Authentication Problems
- Confirm JWT tokens are being stored and retrieved correctly
- Check that tokens are properly formatted in Authorization headers
- Verify token expiration handling

### Styling Issues
- Ensure Tailwind CSS is properly configured
- Check that global styles are loaded correctly
- Verify component styling classes are properly applied