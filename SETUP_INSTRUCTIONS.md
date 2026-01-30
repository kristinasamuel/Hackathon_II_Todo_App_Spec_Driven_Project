# AI Chatbot Setup Instructions

## Required Configuration

To make the AI Chatbot fully functional, you need to add your actual Gemini API key.

### Step 1: Get a Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create an account or sign in
3. Create a new API key for the Gemini API
4. Copy the API key

### Step 2: Configure the Backend
1. Open `phase-3-Ai-Chatbot/backend/.env`
2. Replace the placeholder with your actual Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```
3. Save the file

### Step 3: Restart the Servers
After updating the API key, restart both servers:
```bash
# In phase-3-Ai-Chatbot/backend directory:
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# In phase-3-Ai-Chatbot/frontend_new directory:
npm run dev
```

## Available Endpoints

### Backend API
- Base URL: http://localhost:8000
- Chat endpoint: http://localhost:8000/api/chat
- API Documentation: http://localhost:8000/docs

### Frontend Pages
- Main site: http://localhost:3000
- AI Chatbot page: http://localhost:3000/ai-chatbot
- Login: http://localhost:3000/login
- Dashboard: http://localhost:3000/dashboard

## Using the AI Chatbot

1. Navigate to http://localhost:3000 and log in
2. Click on "AI Chatbot" in the header navigation
3. Start chatting with the bot using natural language:
   - "Add a task to buy groceries"
   - "Show me my tasks"
   - "Complete task 1"
   - "Delete the meeting task"
   - "Update task 1 to call John tomorrow"

## Troubleshooting

### Common Issues:

1. **"400 API key not valid" Error**: Make sure you've added a valid Gemini API key to the .env file
2. **Page redirects**: Ensure you're logged in before accessing the AI Chatbot page
3. **Connection timeouts**: Verify both backend and frontend servers are running

### Verification Steps:
1. Check that the backend server is running on port 8000
2. Check that the frontend server is running on port 3000
3. Verify the GEMINI_API_KEY in the .env file is valid
4. Confirm you can access the API documentation at http://localhost:8000/docs