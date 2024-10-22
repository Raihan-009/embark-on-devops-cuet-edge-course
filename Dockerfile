# Use nginx:alpine as base image (lightweight)
FROM nginx:alpine

# Copy static files to nginx html directory
COPY html/ /usr/share/nginx/html/

# Nginx runs on port 80 by default
EXPOSE 80

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]