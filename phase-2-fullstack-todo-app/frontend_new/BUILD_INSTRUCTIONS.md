# Build Instructions for Todo App Frontend

## Local Build Process

To build the project locally and ensure it will build successfully on Vercel:

### 1. Prerequisites
- Node.js 16+ installed
- npm or yarn package manager

### 2. Setup Environment
```bash
# Navigate to the frontend directory
cd frontend_new

# Install dependencies
npm install

# Set environment variables for local build test
echo "NEXT_PUBLIC_API_BASE_URL=http://localhost:8000" > .env.local
```

### 3. Test the Build Locally
```bash
# Run the build command (this simulates Vercel's build process)
npm run build
```

Expected output should end with:
```
✓ Built in [time]
○ Generating static pages (0/0)

Done in [time]s.
```

### 4. Verify Build Success
After a successful build, you should see:
- No error messages during the build process
- A `out` directory created (for static export) or `.next` directory
- All pages compiled successfully

## Common Build Errors and Solutions

### Error: Cannot resolve dependency
**Cause**: Missing dependency or incorrect import path
**Solution**:
```bash
npm install [missing-package]
# or
npm install
```

### Error: Environment variable not defined
**Cause**: Missing environment variable
**Solution**: Ensure `NEXT_PUBLIC_API_BASE_URL` is set

### Error: Module not found
**Cause**: Incorrect import path
**Solution**: Check import statements and file paths

## Vercel Build Process

Vercel will execute the following commands during deployment:

1. `npm install` - Install dependencies
2. `npm run build` - Build the application
3. Serve the built application

## Pre-deployment Checklist

Before deploying to Vercel, ensure:

- [ ] `npm run build` completes without errors locally
- [ ] All environment variables are properly configured
- [ ] Backend API is accessible at the configured URL
- [ ] CORS is properly configured on the backend
- [ ] All assets are properly referenced
- [ ] No sensitive information is hardcoded in the source

## Optimizing for Vercel Build

### 1. Minimize Dependencies
- Remove unused packages
- Use lightweight alternatives where possible

### 2. Optimize Images
- Use modern formats (WebP, AVIF)
- Implement proper image optimization with Next.js Image component

### 3. Code Splitting
- Use dynamic imports for heavy components
- Leverage Next.js automatic code splitting

## Testing Build Locally

```bash
# Clean any previous builds
rm -rf .next out

# Install fresh dependencies
npm ci  # Use ci for clean install

# Build the project
npm run build
```

## Troubleshooting Build Issues

### If build fails:
1. Check the error message carefully
2. Look for missing environment variables
3. Verify all imports are correct
4. Check for syntax errors in configuration files
5. Ensure all dependencies are properly installed

### For debugging:
```bash
# Verbose build output
npm run build --verbose

# Check for dependency issues
npm ls
```

## Deployment Optimization Tips

1. **Keep build time under 10 minutes** - Vercel has build timeouts
2. **Minimize node_modules size** - Use `.dockerignore` or similar
3. **Use Next.js features** - Automatic optimizations like Image, Link, etc.
4. **Leverage caching** - Use proper cache headers and static generation