# Dockerfile for Frontend (Next.js application)
# Stage 1: Build the Next.js application
FROM node:20-alpine AS builder

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package.json yarn.lock* package-lock.json* ./

# Install dependencies
RUN npm install --frozen-lockfile

# Copy the rest of the application code
COPY . .

# Build the Next.js application
# 'npm run build' will typically create an optimized production build in the '.next' directory
RUN npm run build

# Stage 2: Serve the Next.js application
FROM node:20-alpine

WORKDIR /app

# Copy necessary files from the builder stage
COPY --from=builder /app/next.config.ts ./next.config.ts
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# Expose the port Next.js typically runs on
EXPOSE 3000

# Command to run the application in production mode
CMD ["npm", "start"]
