import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from pymongo import MongoClient
from django.conf import settings

# Establish MongoDB connection
class MongoDBConnection:
    def __init__(self):
        self.client = MongoClient(settings.DATABASES['default']['HOST'])
        self.db = self.client[settings.DATABASES['default']['NAME']]

    def get_collection(self, collection_name):
        return self.db[collection_name]

# User Registration View
@csrf_exempt
def UserRegister(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON request body
            userData = json.loads(request.body)
            # Access the data
            user_name = userData.get('userData', {}).get('username')
            user_email = userData.get('userData', {}).get('useremail')
            user_password = userData.get('userData', {}).get('userpassword')

            # Field validation: check if any field is missing
            if not user_name or not user_email or not user_password:
                return JsonResponse({'error': 'All fields are required (username, useremail, userpassword)'},
                                    status=400)

            # Hash the password
            hashed_password = make_password(user_password)

            # Create a MongoDB connection and get the collection
            mongo_conn = MongoDBConnection()
            users_collection = mongo_conn.get_collection('users')  # Replace 'users' with your actual collection name

            # Check if the username or email already exists
            existing_user = users_collection.find_one({'username': user_name})
            if existing_user:
                return JsonResponse({'error': 'Username already exists'}, status=400)

            existing_email = users_collection.find_one({'email': user_email})
            if existing_email:
                return JsonResponse({'error': 'Email already exists'}, status=400)

            # Create a new user document
            new_user = {
                'username': user_name,
                'email': user_email,
                'password': hashed_password
            }

            # Insert the new user into the database
            users_collection.insert_one(new_user)

            # Respond with success message
            return JsonResponse({'message': 'Registration successful', 'data': userData}, status=200)

        # Handle JSON decode error
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON input'}, status=400)
        # Handle any other exception
        except Exception as e:
            print(f"Error occurred: {str(e)}")  # For debugging
            return JsonResponse({'error': 'An error occurred during registration'}, status=500)
    else:
        # Respond with error if the request method is not POST
        return JsonResponse({'error': 'Invalid request method. Only POST allowed.'}, status=405)
