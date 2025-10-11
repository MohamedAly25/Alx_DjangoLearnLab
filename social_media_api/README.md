# Social Media API

A comprehensive REST API for a social media platform built with Django and Django REST Framework.

## Features

- User authentication (register, login, profile management)
- Posts and comments with CRUD operations
- User follows and personalized feed
- Likes on posts with notifications
- Notifications for likes, follows, and comments

## API Endpoints

### Authentication
- `POST /api/register/` - Register a new user
- `POST /api/login/` - Login and get token
- `GET/PUT /api/profile/` - View/update profile

### Posts
- `GET /api/posts/` - List posts (paginated, searchable)
- `POST /api/posts/` - Create post
- `GET /api/posts/{id}/` - Retrieve post
- `PUT/PATCH /api/posts/{id}/` - Update post
- `DELETE /api/posts/{id}/` - Delete post
- `POST /api/posts/{id}/like/` - Like a post
- `POST /api/posts/{id}/unlike/` - Unlike a post

### Comments
- `GET /api/comments/` - List comments
- `POST /api/comments/` - Create comment
- `GET /api/comments/{id}/` - Retrieve comment
- `PUT/PATCH /api/comments/{id}/` - Update comment
- `DELETE /api/comments/{id}/` - Delete comment

### Social Features
- `POST /api/follow/{user_id}/` - Follow a user
- `POST /api/unfollow/{user_id}/` - Unfollow a user
- `GET /api/feed/` - Get personalized feed

### Notifications
- `GET /api/notifications/` - List notifications
- `PATCH /api/notifications/{id}/` - Mark notification as read

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment: `.venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Run the server: `python manage.py runserver`

## Deployment

This project is configured for deployment on Heroku.

### Environment Variables
Set the following environment variables in your deployment platform:

- `SECRET_KEY`: Django secret key
- `DEBUG`: False for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_ENGINE`: django.db.backends.postgresql
- `DATABASE_NAME`: Database name
- `DATABASE_USER`: Database user
- `DATABASE_PASSWORD`: Database password
- `DATABASE_HOST`: Database host
- `DATABASE_PORT`: Database port

### Files for Deployment
- `requirements.txt`: Python dependencies
- `Procfile`: Heroku process file
- `runtime.txt`: Python version specification

## Testing

Use tools like Postman or curl to test the API endpoints. Authentication requires tokens obtained from the login endpoint.

## License

This project is for educational purposes.