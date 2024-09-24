from mailjet_rest import Client
import base64

api_key = 'API_KEY'
api_secret = 'SECRET_KEY'

mailjet = Client(auth=(api_key, api_secret), version='v3.1')

def sendMail(file_path, to, name):
    try:
        # Read and encode the attachment file
        with open(file_path, 'rb') as file:
            encoded_file = base64.b64encode(file.read()).decode()

        # Prepare email data
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "aditya2kumar465625@gmail.com",
                        "Name": "Aditya Kumar"
                    },
                    "To": [
                        {
                            "Email": to,
                            "Name": name
                        }
                    ],
                    "Subject": "Your Certificate",
                    "TextPart": f"Dear {name},\nPlease find your certificate attached.",
                    "HTMLPart": f"<h3>Dear {name},</h3><p>Your certificate is attached below.</p>",
                    "CustomID": "CertificateEmailTest",
                    "Attachments": [
                        {
                            "ContentType": "image/png",
                            "Filename": "certificate.png",  # You can make this dynamic
                            "Base64Content": encoded_file
                        }
                    ]
                }
            ]
        }

        # Send email
        result = mailjet.send.create(data=data)
        print(f"Status Code: {result.status_code}")
        print(result.json())

    except Exception as e:
        print(f"An error occurred: {e}")

# Usage example
# sendMail('/path/to/your/certificate.png', 'recipient@example.com', 'Recipient Name')
