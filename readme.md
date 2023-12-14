Application Setup Instructions
This README outlines the steps to get your backend and frontend services running using Docker.

Prerequisites
Docker
Docker Compose
Docker Desktop (for local development on Windows or Mac)
Getting Started
Launch Services

To build and start all services as defined in your Docker Compose file, run the following command in the root directory of your project:

sh
Copy code
docker-compose up
This command will build the Docker images for your services if they don't exist or are outdated and start the containers.

Install Docker Desktop

If you haven't already installed Docker Desktop, please download and install it from the official Docker website.

Backend
The backend service is a Python API using FastAPI.

Access the backend API at http://localhost:5040.

Modify source files in the backend/src directory as needed.

To add a new library, update the requirements.txt file in the src folder, and it will be installed automatically.

Changes made to the source files will auto-save and the application will reload to reflect these changes.

The backend uses the FastAPI framework. You can find the documentation for FastAPI here.

Frontend
The frontend service can be accessed through your web browser.

Open the frontend URL: http://localhost:8080/.
Running Frontend Commands
To install dependencies:

sh
Copy code
docker-compose exec frontend npm install
To change source files, modify the files within the frontend/src directory.

To build the frontend application after changes:

sh
Copy code
docker-compose exec frontend npm run build
(Note: There seems to be a redundant command in the instructions: docker compose exec frontend npm run install should probably just be docker compose exec frontend npm install. Ensure you're using the correct command.)

Additional Notes
Ensure Docker is running before executing any docker-compose commands.
For changes to take effect in Docker containers, volumes should be correctly mapped to the host.
Troubleshooting
If you encounter any issues, please check the Docker and Docker Compose documentation, or access the logs of each service using:

sh
Copy code
docker-compose logs [service_name]
Replace [service_name] with backend or frontend as needed.