# Todo Application - Frontend Quick Start Guide

## Prerequisites

- Node.js (version 18 or higher)
- npm or yarn package manager
- Access to the backend API server

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd phase-2 -full stack todo app/frontend
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Environment Configuration
Create a `.env.local` file in the frontend root directory:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Replace `http://localhost:8000` with your actual backend API URL.

## Development Setup

### 1. Start the Development Server
```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`

### 2. Backend Connection
Make sure your backend server is running before starting the frontend. The default backend URL is `http://localhost:8000`.

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── login/            # Login page
│   ├── signup/           # Signup page
│   ├── dashboard/        # Dashboard page
│   ├── layout.tsx        # Root layout
│   └── page.tsx          # Homepage
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── auth/        # Authentication components
│   │   └── tasks/       # Task management components
│   ├── services/         # API and business logic
│   ├── hooks/            # Custom React hooks
│   └── utils/            # Utility functions
├── public/               # Static assets
├── package.json
└── tailwind.config.js
```

## Key Features

### Authentication
- Navigate to `/login` to sign in
- Navigate to `/signup` to create an account
- Authentication state is managed automatically

### Task Management
- Visit `/dashboard` to manage your tasks
- Create new tasks using the form
- Update, delete, or mark tasks as complete

## API Integration

The frontend communicates with the backend through the following endpoints:

- Authentication: `/auth/login`, `/auth/register`
- Tasks: `/api/{user_id}/tasks/*`

API calls automatically include JWT tokens in the Authorization header.

## Building for Production

```bash
npm run build
npm start
```

Or with Docker:
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Verify the backend server is running
   - Check that `NEXT_PUBLIC_API_BASE_URL` is correctly set

2. **Authentication Problems**
   - Clear browser storage if experiencing token issues
   - Verify JWT token format and expiration

3. **Development Server Won't Start**
   - Check Node.js version requirement
   - Clear npm cache: `npm cache clean --force`
   - Delete node_modules and reinstall dependencies

### Useful Commands

```bash
# Run development server
npm run dev

# Build for production
npm run build

# Run linter
npm run lint

# Run tests
npm test
```

## Next Steps

1. Customize the UI to match your branding
2. Add additional features as needed
3. Set up CI/CD pipeline for deployment
4. Configure monitoring and error reporting