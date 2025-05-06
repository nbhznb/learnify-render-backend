# Learnify Backend

This is the backend for the Learnify web application, built using Flask. It serves as an API to handle quiz-related requests from the frontend. The backend generates questions for various categories, including non-verbal reasoning, spatial reasoning, English, maths, and verbal reasoning. Additionally, it provides routes for user registration, login, profile management, and user deletion, as well as administrative features for user approval and subscription management.

## Features
- Serves quiz questions for various categories
- Generates images dynamically for non-verbal reasoning and spatial reasoning questions
- Handles diagram drawing requests
- Cleans up temporary images to manage storage efficiently
- User registration, login, profile management, and deletion
- Admin functionalities for approving and canceling user subscriptions

## Technologies Used
- **Flask** - Web framework
- **Flask-CORS** - Handling CORS for frontend communication
- **Flask-SQLAlchemy** - ORM for database interactions
- **Flask-Bcrypt** - Password hashing
- **Flask-JWT-Extended** - JSON Web Token for authentication
- **OpenCV (cv2)** - Image processing
- **Matplotlib** - Generating diagrams
- **NumPy** - Numerical operations
- **Pillow** - Image manipulation
- **SQLAlchemy-Utils** - Database utility functions
- **PostgreSQL** - Relational database management system
- **Gunicorn** - WSGI HTTP Server for production deployment

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- PostgreSQL

### Setup Instructions

#### Local Development

1. Clone the repository:
   ```sh
   git clone <your-repo-url>
   cd <your-repo-folder>/backend
   ```

2. Create a virtual environment and activate it:
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database:
   - Ensure PostgreSQL is installed and running:
   ```sh
   sudo service postgresql start  # Linux
   # Or use pgAdmin or other tools on Windows/macOS
   ```
   - Create a database and user for the application:
   ```sh
   sudo -u postgres psql
   CREATE DATABASE learnify;
   CREATE USER learnify_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE learnify TO learnify_user;
   \q
   ```

5. Set environment variables:
   ```sh
   export DATABASE_URL="postgresql://learnify_user:your_password@localhost/learnify"
   export SECRET_KEY="your_secret_key"
   export ADMIN_PASSKEY="your_admin_passkey"
   export PYTHONPATH=$(pwd)
   ```
   On Windows, use `set` instead of `export`.

#### Docker Development

The recommended way to run the backend is using Docker, as described in the main README.md file. This ensures consistent environments across development and production.

```sh
# From the project root directory
docker-compose up -d web
```

## Configuration

### Environment Variables

The backend uses the following environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secret key for JWT token generation
- `ADMIN_PASSKEY`: Passkey for admin access (default: admin123)
- `FLASK_ENV`: Environment mode (development or production)
- `FLASK_DEBUG`: Enable debug mode (1 for true, 0 for false)

### Admin Passkey

The admin passkey can be changed in the `config.py` file or through environment variables:

1. Open the `src/config.py` file:
   ```python
   ADMIN_PASSKEY = os.getenv('ADMIN_PASSKEY', 'admin123')
   ```

2. Replace `'admin123'` with your desired passkey or set the `ADMIN_PASSKEY` environment variable.

## Running the Application

### Local Development

To start the Flask development server:
```sh
python app.py
```

For production deployment with Gunicorn:
```sh
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

### Docker Deployment

The backend is containerized using Docker. The Dockerfile is configured to:

1. Use Python 3.11 slim as the base image
2. Install dependencies
3. Set up the application
4. Run the application using Gunicorn

To build and run the Docker container:
```sh
# Build the image
docker build -t learnify-backend .

# Run the container
docker run -p 5000:5000 -e DATABASE_URL=postgresql://user:password@db/learnify learnify-backend
```

## Project Structure

```
backend/
├── src/                  # Source code directory
│   ├── __init__.py       # Package initialization
│   ├── auth/             # Authentication related modules
│   ├── models/           # Database models
│   ├── routes/           # API routes
│   ├── services/         # Business logic
│   ├── utils/            # Utility functions
│   └── config.py         # Configuration settings
├── app.py                # Application entry point
├── wsgi.py               # WSGI entry point for production
├── Dockerfile            # Docker configuration
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## API Endpoints

### Health Check Endpoints

#### API Status
- **GET /**
- Returns a diagnostic message indicating the API is running.
- Response: `Learnify API is running. Go to /api/ for endpoints.`

#### Health Check
- **GET /api/health**
- Returns a simple health status of the API.
- Response:
  ```json
  {
    "status": "ok",
    "message": "API is running"
  }
  ```

#### Enhanced Health Check
- **GET /api/healthy**
- Returns a detailed health status including system information and database connectivity.

### Authentication Endpoints

#### User Registration
- **POST /api/auth/user/register**
- Registers a new user with username, email, and password.
- Request body:
  ```json
  {
    "username": "example_user",
    "email": "user@example.com",
    "password": "secure_password"
  }
  ```
- Response:
  ```json
  {
    "message": "User registered successfully"
  }
  ```

#### User Login
- **POST /api/auth/user/login**
- Logs in a user with username and password, returning a JWT token.
- Request body:
  ```json
  {
    "username": "example_user",
    "password": "secure_password"
  }
  ```
- Response:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "username": "example_user",
      "email": "user@example.com"
    }
  }
  ```

### Quiz Endpoints

#### Non-Verbal Reasoning Questions
- **GET /api/questions/nvr**
- Returns a randomly generated non-verbal reasoning question.

#### Spatial Reasoning Questions
- **GET /api/questions/spatial**
- Returns a randomly generated spatial reasoning question.

#### English Questions
- **GET /api/questions/english**
- Fetches English quiz data from a JSON file.

#### Maths Questions
- **GET /api/questions/maths**
- Fetches Maths quiz data from a JSON file.

#### Verbal Reasoning Questions
- **GET /api/questions/vr**
- Fetches Verbal Reasoning quiz data from a JSON file.

#### Diagram Generation
- **POST /api/questions/diagram**
- Generates a diagram based on provided parameters.
- Request body: JSON with diagram specifications.

### User Management Endpoints

#### User Profile
- **GET /api/auth/user/profile**
- Retrieves the profile of the logged-in user.
- **PUT /api/auth/user/profile**
- Updates the profile of the logged-in user.
- **DELETE /api/auth/user/profile**
- Deletes the profile of the logged-in user.

### Admin Endpoints

#### Admin Panel
- **GET /api/admin**
- Displays the admin panel and a login form if the admin is not authenticated.
- **POST /api/admin**
- Allows the admin to log in using a passkey.

#### Admin Logout
- **GET /api/admin/logout**
- Logs out the admin.

#### Admin Approve User
- **POST /api/admin/approve**
- Approves a user's subscription for a specified duration.
- Requires JSON data with `user_id` and `duration` (e.g., "1 month", "3 months").

#### Admin Cancel User Subscription
- **POST /api/admin/cancel**
- Cancels a user's subscription.
- Requires JSON data with `user_id`.

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Error: "Could not connect to the database"
   - Solution: Ensure PostgreSQL is running and the DATABASE_URL is correct
   
   ```sh
   # Check if PostgreSQL is running
   sudo service postgresql status
   
   # Verify connection string
   psql "postgresql://learnify_user:your_password@localhost/learnify"
   ```

2. **Module Import Errors**
   - Error: "ModuleNotFoundError: No module named 'src'"
   - Solution: Set the PYTHONPATH environment variable
   
   ```sh
   export PYTHONPATH=$(pwd)
   ```

3. **Docker-related Issues**
   - Error: "Error starting userland proxy"
   - Solution: Check if port 5000 is already in use
   
   ```sh
   # Check ports in use
   netstat -tuln | grep 5000
   
   # Kill process using port 5000
   kill $(lsof -t -i:5000)
   ```

4. **JWT Token Issues**
   - Error: "Signature verification failed"
   - Solution: Ensure the SECRET_KEY is consistent across restarts
   
   ```sh
   # Set a permanent SECRET_KEY in your environment
   echo 'export SECRET_KEY="your_consistent_secret_key"' >> ~/.bashrc
   source ~/.bashrc
   ```

## Development Tips

### Database Migrations

If you make changes to the database models, you'll need to create and apply migrations:

```sh
# Initialize migrations (first time only)
flask db init

# Create a migration
flask db migrate -m "Description of changes"

# Apply the migration
flask db upgrade
```

### Testing the API

You can use curl or tools like Postman to test the API endpoints:

```sh
# Basic health check
curl http://localhost:5000/

# Get health status
curl http://localhost:5000/api/health

# Test user registration
curl -X POST http://localhost:5000/api/auth/user/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test_user","email":"test@example.com","password":"password123"}'

# Test user login
curl -X POST http://localhost:5000/api/auth/user/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test_user","password":"password123"}'

# Get English questions
curl http://localhost:5000/api/questions/english

# Get Maths questions
curl http://localhost:5000/api/questions/maths

# Get Verbal Reasoning questions
curl http://localhost:5000/api/questions/vr

# Get Non-verbal Reasoning questions
curl http://localhost:5000/api/questions/nvr

# Get Spatial Reasoning questions
curl http://localhost:5000/api/questions/spatial

# Test protected endpoint (with JWT token)
curl -X GET http://localhost:5000/api/auth/user/profile \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Acknowledgements
This project incorporates and improves upon functions originally developed in the [Non-Verbal Reasoning](https://github.com/hardiksurana/non-verbal-reasoning) project by Hardik Surana and collaborators.

## License
This project follows an open-source license. Check the repository for more details.

## Deployment on Render.com

This application is configured for easy deployment on Render.com:

### Deployment Steps

1. **Prepare the Application for Render.com**
   - Switch to SQLite for simpler deployment (no separate database service needed)
   - Create a global Flask application instance for Gunicorn to use
   ```python
   # In app.py, add:
   app = create_app()
   ```
   - Create the following configuration files:
     - `render.yaml`: Defines services and environment variables
     - `runtime.txt`: Specifies Python version 
     - `Procfile`: Defines the web service command

2. **Sign up for Render**
   - Create an account at [render.com](https://render.com)

3. **Create a new Web Service**
   - Click "New +" and select "Web Service"
   - Connect your GitHub/GitLab repository 
   - Select the repository containing this code

4. **Configure the Web Service**
   - Render will automatically detect the Python application
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

5. **Environment Variables**
   - Render automatically sets `RENDER_EXTERNAL_URL` and other variables
   - Add these additional variables in the dashboard:
     - `SECRET_KEY` (Generate a secure random string)
     - `JWT_SECRET_KEY` (Generate another secure random string)
     - `DEBUG` = `False`
     - `CORS_ORIGINS` = Your frontend URL (or `*` for development)

6. **Database Setup**
   - For development: Uses SQLite by default (stored in the app's file system)
   - For production: Consider adding a PostgreSQL database via Render
     - Create a PostgreSQL service in Render
     - Connect it to your Web Service
     - Render will set `DATABASE_URL` automatically

7. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy your application

8. **Verify Deployment**
   - Check if your app is accessible at `https://your-service-name.onrender.com`
   - Test the health endpoint: `https://your-service-name.onrender.com/api/health`
   - Test the English questions endpoint: `https://your-service-name.onrender.com/api/questions/english`

9. **Troubleshooting**
   - If deployment fails, check Render's logs in the dashboard
   - Common issues:
     - Incorrect start command (should be `app:app` not `app:create_app()`)
     - Missing dependencies in requirements.txt
     - Environment variables not set correctly

Your application will be available at `https://your-service-name.onrender.com`
