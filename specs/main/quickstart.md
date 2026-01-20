# Quickstart Guide: TaskManager Pro - Phase II Frontend

## Overview
This guide provides instructions to quickly set up and run the TaskManager Pro frontend application. The frontend connects to an existing backend API to provide a professional task management interface.

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Access to the TaskManager Pro backend API (running on http://localhost:8000 by default)
- Git for cloning the repository

## Setup Instructions

### 1. Clone the Repository
```bash
git clone [repository-url]
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

Adjust the API URL if your backend is running on a different port or location.

### 4. Run the Development Server
```bash
npm run dev
# or
yarn dev
```

The application will be available at http://localhost:3000

## Project Structure
```
frontend/
├── app/                    # Next.js App Router pages
│   ├── login/            # Login page
│   ├── signup/           # Signup page
│   ├── dashboard/        # Dashboard page with task management
│   ├── layout.tsx        # Root layout
│   └── page.tsx          # Home/landing page
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── auth/        # Authentication components
│   │   ├── tasks/       # Task management components
│   │   └── ui/          # General UI components
│   ├── services/         # API and business logic services
│   │   ├── api.ts       # API service with JWT handling
│   │   ├── auth.ts      # Authentication service
│   │   └── tasks.ts     # Task service
│   ├── hooks/            # Custom React hooks
│   │   ├── useAuth.ts   # Authentication hook
│   │   └── useTasks.ts  # Task management hook
│   └── utils/            # Utility functions
├── public/               # Static assets
├── package.json          # Dependencies and scripts
└── tailwind.config.js    # Tailwind CSS configuration
```

## Key Features

### Authentication
- **Signup**: Create a new account with email and password
- **Login**: Authenticate using email and password
- **JWT Token Management**: Secure token storage and automatic inclusion in API requests
- **Protected Routes**: Dashboard and task management only accessible to authenticated users

### Task Management
- **Create Tasks**: Add new tasks with title and optional description
- **View Tasks**: See all your tasks in a clean, organized format
- **Update Tasks**: Edit task details as needed
- **Complete/Incomplete**: Mark tasks as complete or revert to active
- **Delete Tasks**: Remove tasks you no longer need

### UI/UX Features
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Loading States**: Visual feedback during API operations
- **Error Handling**: Clear error messages for various failure scenarios
- **Success Feedback**: Notifications for successful operations

## API Integration
The frontend communicates with the backend API using these endpoints:
- Authentication: `/auth/login`, `/auth/register`
- Tasks: `/api/{user_id}/tasks/*`

All authenticated requests automatically include the JWT token in the Authorization header as `Bearer {token}`.

## Running in Production
To build and run the application for production:

```bash
npm run build
npm start
```

## Troubleshooting

### Common Issues
1. **Backend Connection Issues**:
   - Ensure the backend API is running
   - Verify the NEXT_PUBLIC_API_BASE_URL is correctly set
   - Check CORS settings if running on different ports

2. **Authentication Issues**:
   - Clear browser storage if authentication state becomes inconsistent
   - Ensure the backend authentication endpoints are accessible

3. **Build Issues**:
   - Clear npm/yarn cache if encountering build errors
   - Verify all dependencies are installed

### Development Tips
- Use the Next.js development server for hot reloading
- Check browser developer tools for API response inspection
- Monitor the console for error messages during development

## Next Steps
1. Customize the UI to match your branding requirements
2. Add additional features based on your specific needs
3. Implement additional security measures if required
4. Set up automated testing for your specific use cases