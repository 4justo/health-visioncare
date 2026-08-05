FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy application
COPY frontend .

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
# Use root for local dev so Vite can write build artifacts into the mounted project directory
USER root

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]