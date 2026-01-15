# TodoApp Frontend

This is the frontend for the TodoApp, built with Next.js 16+, TypeScript, and Tailwind CSS. It provides a responsive, professional UI for managing tasks with secure authentication.

## Features

- **Secure Authentication**: JWT-based authentication with refresh token handling
- **Task Management**: Create, read, update, and delete tasks
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Professional UI**: Clean, modern interface with consistent design
- **Error Handling**: Comprehensive error handling and user feedback
- **Accessibility**: Built with accessibility in mind

## Tech Stack

- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript 5.x
- **Styling**: Tailwind CSS 3.x
- **HTTP Client**: Axios
- **State Management**: React hooks
- **Testing**: Jest, React Testing Library

## Prerequisites

- Node.js 18+
- npm or yarn package manager
- Access to the backend API (running on `http://localhost:8000` by default)

## Setup

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Navigate to the frontend directory**:
   ```bash
   cd phase-2 -full stack todo app/frontend
   ```

3. **Install dependencies**:
   ```bash
   npm install
   ```

4. **Create environment file**:
   ```bash
   cp .env.example .env.local
   ```

   Update the `.env.local` file with your configuration:
   ```
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```

5. **Start the development server**:
   ```bash
   npm run dev
   ```

6. **Open your browser** to [http://localhost:3000](http://localhost:3000)

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: Base URL for the backend API (required)
- `NEXT_PUBLIC_BACKEND_URL`: Backend URL for other integrations (optional)

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter
- `npm run test` - Run tests
- `npm run test:watch` - Run tests in watch mode

## Project Structure

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
│   │   ├── api.ts         # API service with JWT handling
│   │   ├── auth.ts        # Authentication service
│   │   └── tasks.ts       # Task service
│   ├── hooks/             # Custom React hooks
│   ├── utils/             # Utility functions
│   │   ├── logger.ts      # Comprehensive logging utility
│   │   └── jwt.ts         # JWT utilities
│   └── styles/            # Styling
│       └── globals.css    # Global styles
├── public/                # Static assets
├── package.json          # Dependencies and scripts
├── next.config.js        # Next.js configuration
├── tailwind.config.js    # Tailwind CSS configuration
└── tsconfig.json         # TypeScript configuration
```

## API Integration

The frontend communicates with the backend API located at:
- Base URL: `http://localhost:8000` (or as configured in environment variables)
- Authentication endpoints: `/auth/*`
- Task endpoints: `/api/{user_id}/tasks`

All authenticated requests include the JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Authentication Flow

1. User visits `/login` or `/signup` page
2. Credentials are sent to backend authentication endpoint
3. JWT token is received and stored in browser storage
4. Token is included in all subsequent API requests
5. Token expiration is monitored and refresh is handled automatically

## Error Handling

The application implements comprehensive error handling:

- Network connectivity issues
- JWT token expiration with automatic refresh
- Unauthorized resource access attempts
- Backend API unavailability
- User-friendly error messages

## Testing

Run the test suite with:
```bash
npm run test
```

For tests in watch mode:
```bash
npm run test:watch
```

## Deployment

1. Build the application:
   ```bash
   npm run build
   ```

2. Start the production server:
   ```bash
   npm start
   ```

## Security Considerations

- JWT tokens are stored securely in browser storage
- All API requests include proper authentication headers
- Token refresh mechanism prevents session expiration
- Input validation is performed on the backend
- CORS policies are configured on the backend

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

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request