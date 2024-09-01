from firebase_functions import https_fn, options
from firebase_admin import firestore
import base64, os, json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials

load_dotenv()


# cred = credentials.Certificate(
#     "/Users/vogo/Documents/Personal/pharmaquickbill/keys/pharmaquickbill-firebase-adminsdk-facg6-8c8fc3c99a.json")

def get_service_account():
    # Retrieve the base64 encoded service account key from environment variables
    encoded_key = os.getenv('SERVICE_ACCOUNT_KEY')
    if encoded_key:
        service_account_info = base64.b64decode(encoded_key).decode('utf-8')
        service_account_dict = json.loads(service_account_info)
        # Pass the dictionary to the Certificate constructor
        return credentials.Certificate(service_account_dict)
    else:
        raise ValueError("Service account credentials not found in environment variables")


cred = get_service_account()

firebase_admin.initialize_app(cred)

db = firestore.client()


@https_fn.on_request(
    cors=options.CorsOptions(
        cors_origins=["*"],
        cors_methods=["get", "post"],
    )
)
def contact_us(req: https_fn.Request) -> https_fn.Response:
    # Check if the request method is POST
    if req.method == "POST":
        # Assume the POST data is JSON
        post_data = req.json

        # Extract variables from the JSON data
        name = post_data.get("name")
        email = post_data.get("email")
        phone = post_data.get("phone")
        store_name = post_data.get("store_name")
        message = post_data.get("message")

        # Create a document in Firestore
        db.collection('contacts').add({
            'name':name,
            'email': email,
            'phone': phone,
            'store_name': store_name,
            'message':message,
            'timestamp': firestore.SERVER_TIMESTAMP
        })

        # Return a success response
        return https_fn.Response(
            f"Data stored successfully: Email - {email}, Phone - {phone}, Store Name - {store_name}",
            status=201
        )

    return https_fn.Response("Hello world!", status=200)
