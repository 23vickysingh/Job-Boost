# --- Stage 1: Build the React App ---
FROM node:20-alpine AS builder

# Set the working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY FrontEnd/package.json FrontEnd/package-lock.json ./
RUN npm install

# Copy the rest of the frontend code
COPY FrontEnd/ .

# Build the application for production
RUN npm run build

# --- Stage 2: Serve the App with Nginx ---
FROM nginx:stable-alpine

# Copy the built static files from the 'builder' stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy the custom Nginx configuration from the FrontEnd directory
COPY FrontEnd/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]