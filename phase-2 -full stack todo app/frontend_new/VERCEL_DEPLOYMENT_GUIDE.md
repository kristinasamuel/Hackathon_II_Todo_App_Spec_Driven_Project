# Vercel Deployment Guide for Todo App Frontend

This guide provides step-by-step instructions to successfully deploy your Next.js frontend to Vercel without encountering build errors.

## Prerequisites

- A working GitHub/GitLab/Bitbucket repository with your frontend code
- A deployed backend API (either on Vercel, Heroku, Railway, or any hosting service)
- Valid domain for your backend API

## Pre-deployment Checklist

Before deploying to Vercel, ensure:

1. ✅ Backend API is deployed and accessible via HTTPS
2. ✅ CORS is configured to allow requests from your Vercel domain
3. ✅ All environment variables are properly configured
4. ✅ Frontend builds successfully locally (`npm run build`)

## Step-by-Step Deployment

### 1. Prepare Your Repository

Make sure your repository contains:
- All necessary source files
- `package.json` and `package-lock.json` (or `yarn.lock`)
- `next.config.ts` with proper configuration
- `.gitignore` properly set up

### 2. Vercel Account Setup

1. Go to [vercel.com](https://vercel.com) and create an account
2. Install the Vercel CLI (optional): `npm i -g vercel`

### 3. Import Your Project to Vercel

1. Log in to Vercel dashboard
2. Click "New Project"
3. Select your Git provider (GitHub, GitLab, Bitbucket)
4. Choose your repository containing the frontend code

### 4. Configure Build Settings

In the project settings, ensure the following:

- **Framework Preset**: Next.js (should be auto-detected)
- **Build Command**: `npm run build` (or leave empty to use default)
- **Output Directory**: `out` (if using static export) - typically auto-detected
- **Install Command**: `npm install` (or leave empty to use default)

### 5. Set Environment Variables

Go to Project Settings > Environment Variables and add:

```
NEXT_PUBLIC_API_BASE_URL = https://kristinasamuel-todo-app-deploy.hf.space
```

Replace with your actual backend API URL. In this case, the backend is deployed on Hugging Face Spaces.

### 6. Common Build Error Prevention

To avoid common build errors:

#### A. Ensure Proper API URL Format
- Use HTTPS for production
- Verify the backend domain is accessible
- Test the API endpoints before deployment

#### B. Handle API Failures Gracefully
The application should handle network errors and API failures without crashing.

#### C. Static Site Generation Considerations
If using static export, ensure all dynamic content can be pre-built.

## Troubleshooting Common Issues

### Issue: Build fails due to missing environment variables
**Solution**: Ensure all required environment variables are set in Vercel dashboard

### Issue: API calls fail in production
**Solution**:
1. Check that `NEXT_PUBLIC_API_BASE_URL` is set correctly
2. Verify CORS settings on your backend
3. Ensure backend is accessible via HTTPS

### Issue: Assets not loading properly
**Solution**: Check image domains configuration in `next.config.ts`

### Issue: Redirects or rewrites not working
**Solution**: Verify rewrite rules in `next.config.ts` are properly configured

## Post-Deployment Verification

After deployment, verify:

1. ✅ Website loads without errors
2. ✅ Authentication (login/signup) works
3. ✅ API calls are successful
4. ✅ All pages load correctly
5. ✅ Responsive design works on mobile

## Environment Variables Reference

Required environment variables for production:

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_BASE_URL` | Backend API URL | `https://my-backend-api.vercel.app` |

## Example Successful Deployment Configuration

**Project Root**: `/` (repository root)
**Build Command**: `npm run build`
**Development Command**: `npm run dev`
**Output Directory**: Auto-detected by Vercel

## Support

If you encounter issues not covered in this guide:

1. Check the Vercel deployment logs
2. Verify your backend API is running and accessible
3. Review CORS configuration on your backend
4. Test API endpoints directly with a tool like Postman

## Notes

- Vercel provides automatic deployments from Git branches
- Preview deployments are created for pull requests
- Production deployment happens when merging to main branch
- You can customize the domain name in Project Settings