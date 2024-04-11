# Use an official Node.js runtime as a parent image
FROM node:21.2.0

# Set the working directory to /app
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package.json ./

# Install project dependencies
RUN npm install

# Copy the rest of your application code
COPY . .

# Expose the port the app runs on
EXPOSE 5173

# Define the command to run your app using CMD which defines your runtime
CMD ["npm", "run", "dev"]
