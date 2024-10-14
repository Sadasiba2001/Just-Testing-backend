import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from pymongo import MongoClient
from django.conf import settings
from types import SimpleNamespace

# Establish MongoDB connection
class MongoDBConnection:
    def __init__(self):
        self.client = MongoClient(settings.DATABASES['default']['HOST'])
        self.db = self.client[settings.DATABASES['default']['NAME']]

    def get_collection(self, collection_name):
        return self.db[collection_name]

@csrf_exempt
def UserLogin(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON request body
            userData = json.loads(request.body)
            print("The user's data is:", request.body)

            # Access the data
            user_email = userData.get('loginData', {}).get('loginemail')
            user_password = userData.get('loginData', {}).get('loginpassword')
            print(f"The user's data is: {user_email} and {user_password}")

            # Field validation: check if any field is missing
            if not user_email or not user_password:
                return JsonResponse({'error': 'All fields are required (loginemail, loginpassword)'}, status=400)

            # Create a MongoDB connection and get the users collection
            mongo_conn = MongoDBConnection()
            users_collection = mongo_conn.get_collection('users')  # Replace 'users' with your actual collection name

            # Checking for email existence
            user = users_collection.find_one({'email': user_email})
            if not user:
                return JsonResponse({'error': 'Email not found'}, status=400)

            # Comparing given password with the email corresponding password
            if check_password(user_password, user['password']):
                mock_user = SimpleNamespace(id=user['_id'])  # '_id' is the unique ID in MongoDB
                # Generate a new token for the user
                token = RefreshToken.for_user(mock_user)
                return JsonResponse({
                    'message': 'Login successful',
                    'refresh': str(token),
                    'access': str(token.access_token),
                    'data': userData
                }, status=200)
            else:
                return JsonResponse({'error': 'Invalid password'}, status=400)

        # Handle JSON decode error
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON input'}, status=400)
        # Handle any other exception
        except Exception as e:
            print(f"Error occurred: {str(e)}")  # For debugging
            return JsonResponse({'error': 'An error occurred during login'}, status=500)
    else:
        # Respond with error if the request method is not POST
        return JsonResponse({'error': 'Invalid request method. Only POST allowed.'}, status=405)
