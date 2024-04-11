# Use an official Node runtime as a parent image
FROM node:21.2.0

# Set the working directory to /app
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install any needed packages
RUN npm i

# Bundle app source
COPY . .

EXPOSE 5173

# Command to run the app
CMD ["npm", "run", "dev"]