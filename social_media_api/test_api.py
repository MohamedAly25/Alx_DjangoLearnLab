import os
import django
import json
import time
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
django.setup()

# Temporarily set DEBUG=False to see actual errors
settings.DEBUG = False

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def test_api():
    client = Client(enforce_csrf_checks=False)

    try:
        # Use unique username to avoid conflicts
        timestamp = str(int(time.time()))
        username = f'testuser{timestamp}'
        email = f'test{timestamp}@example.com'
        
        # Test registration
        print("Testing registration...")
        data = {
            'username': username,
            'email': email,
            'password': 'testpass123'
        }
        print(f"Sending data: {data}")
        response = client.post('/api/register/', data, format='json')
        print(f"Registration status: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        print(f"Response headers: {response.headers}")
        if response.status_code == 201:
            data = response.json()
            token = data['token']
            user_id = data['user']['id']
            print(f"Token: {token}")
            
            # Test login
            print("\nTesting login...")
            login_response = client.post('/api/login/', {
                'username': username,
                'password': 'testpass123'
            }, format='json')
            print(f"Login status: {login_response.status_code}")
            if login_response.status_code == 200:
                login_data = login_response.json()
                print(f"Login successful, token: {login_data['token']}")
            else:
                print(f"Login failed: {login_response.content.decode()}")
                return
                
            # Test creating a post
            print("\nTesting post creation...")
            post_response = client.post('/api/posts/', {
                'title': 'Test Post',
                'content': 'This is a test post content'
            }, format='json', HTTP_AUTHORIZATION=f'Token {token}')
            print(f"Post creation status: {post_response.status_code}")
            if post_response.status_code == 201:
                post_data = post_response.json()
                post_id = post_data['id']
                print(f"Post created with ID: {post_id}")
            else:
                print(f"Post creation failed: {post_response.content.decode()}")
                return
                
            # Test liking the post
            print("\nTesting post liking...")
            like_response = client.post(f'/api/posts/{post_id}/like/', {}, format='json', HTTP_AUTHORIZATION=f'Token {token}')
            print(f"Like status: {like_response.status_code}")
            if like_response.status_code == 200:
                print("Post liked successfully")
            else:
                print(f"Like failed: {like_response.content.decode()}")
                
            # Test getting posts
            print("\nTesting getting posts...")
            posts_response = client.get('/api/posts/', HTTP_AUTHORIZATION=f'Token {token}')
            print(f"Posts list status: {posts_response.status_code}")
            if posts_response.status_code == 200:
                posts_data = posts_response.json()
                print(f"Found {len(posts_data['results'])} posts")
            else:
                print(f"Posts retrieval failed: {posts_response.content.decode()}")
                
            # Test notifications
            print("\nTesting notifications...")
            notifications_response = client.get('/api/notifications/', HTTP_AUTHORIZATION=f'Token {token}')
            print(f"Notifications status: {notifications_response.status_code}")
            if notifications_response.status_code == 200:
                notifications_data = notifications_response.json()
                print(f"Found {len(notifications_data['results'])} notifications")
            else:
                print(f"Notifications retrieval failed: {notifications_response.content.decode()}")
                
        else:
            print(f"Error: {response.content.decode()}")
            return
    except Exception as e:
        print(f"Exception during testing: {e}")
        import traceback
        traceback.print_exc()
        return

    print("\nAll API tests completed successfully!")

if __name__ == '__main__':
    test_api()