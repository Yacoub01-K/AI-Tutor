# Use an official Node runtime as a parent image
FROM node:20

# Set the working directory to /app
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install any needed packages
RUN npm install

# Bundle app source
COPY . .

# Expose port 3000
EXPOSE 5173

# Command to run the app
CMD ["npm", "run", "dev"]