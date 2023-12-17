from datetime import datetime, timedelta
from ultralytics import YOLO
from PIL import Image
import websockets
import asyncio
import socket
import io
import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import threading

load_dotenv()

NOTIFICATION_FREQ = 60 # seconds
LAST_NOTIFIED = datetime.now() - timedelta(seconds=NOTIFICATION_FREQ) 

# To Differentiate Email and Raspberry Pi
class Client:
    def __init__(self, websocket, client_type):
        self.websocket = websocket
        self.client_type = client_type

# # To send emails for detections
class Email:
    def __init__(self, email) -> None:
        self.email = email
        # Subtract one minute so there can be detections when the
        # server detects a human upon bootup
        self.last_notified = datetime.now() - timedelta(seconds=NOTIFICATION_FREQ)

    def __hash__(self):
        return hash(self.email)

    def __eq__(self, other):
        if isinstance(other, Email):
            return self.email == other.email
        return False


# Function to send emails to emails in notify_emails
def send_emails(img):
    EMAIL = os.getenv('EMAIL_ADDR')
    PASSWORD = os.getenv('APP_PASSWD')
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    for email in notify_emails:
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = email.email
        msg['Subject'] = "Human Detected"
        body = MIMEText(f"Detected @ {datetime.now()}", 'plain')
        msg.attach(body)

        image_part = MIMEImage(img.getvalue(), Name='image.png')
        image_part.add_header('Content-Disposition', 'attachment; filename="image.png"')
        msg.attach(image_part)
        server.sendmail(EMAIL, email.email, msg.as_string())

# def send_emails(img=None):
#     server = smtplib.SMTP("smtp.gmail.com",587)
#     server.starttls()
#     server.login(EMAIL, PASSWORD)
#     for email in notiify_emails:

#         if (datetime.now() - email.last_notified).total_seconds() > NOTIFICATION_FREQ:
#             message = """From: %s
#             To: %s
#             Subject: text-message
#             detection
#             """ % (EMAIL, email.email)
#             server.sendmail(EMAIL, email.email, message)
#             email.last_notified = datetime.now()


# Function to remove client
async def remove_client(ws):
    connected_clients.remove(ws)
    print(f"Client removed. Connected clients: {len(connected_clients)}")

# Handler for WebSocket connections
async def websocket_handler(websocket):
    global RPI_CLIENT, LAST_NOTIFIED, NOTIFICATION_FREQ

    # Instantiate Client Class
    client_type = await websocket.recv()
    if type(client_type) is bytes:
        client_type = client_type.decode()
    client = Client(websocket=websocket, client_type=client_type)
    connected_clients.add(client)
    await websocket.send(b'ready')
    
    if client_type == "rpi":
        RPI_CLIENT = client

    print(f"{client_type} client connected.")
    print(f"Connected clients: {len(connected_clients)}")

    try:
        async for message in websocket:
            if type(message) == str: # Raspberry Pi sends bytes so this means this came from a browser
                notify_emails.add(Email(message))
                print("Attemping Add:", message)
                print(len(notify_emails))

            for client in connected_clients:
                # Process image through YOLO NN
                if client.websocket != websocket and client.websocket.open:
                    if client.client_type == "web":
                        io_bytes = io.BytesIO(message)
                        image = Image.open(io_bytes)
                        result = model(image, classes=0, conf=0.75, verbose=False)

                        if len(result[0]) > 0: # If detections were made
                            io_bytes.seek(0)  # Move to the start of the buffer
                            io_bytes.truncate() # Refresh buffer
                            for r in result:
                                im_array = r.plot()
                                im = Image.fromarray(im_array[..., ::-1])

                            im.save(io_bytes, format='JPEG')
                        
                            if ((datetime.now() - LAST_NOTIFIED ).total_seconds() > NOTIFICATION_FREQ) and len(notify_emails) > 0:
                                email_thread = threading.Thread(target=send_emails, args=(io_bytes,))
                                email_thread.start()
                                
                                LAST_NOTIFIED = datetime.now()
                            # im = result[0].plot()
                            # cv2.imencode('.JPEG', im)

                        io_bytes.seek(0)
                        frame_data = io_bytes.read()


                        await client.websocket.send(frame_data)
                        await RPI_CLIENT.websocket.send("ready") # move this
                    

    except websockets.exceptions.ConnectionClosedError as e:
        print("DEBUG:", e)
    finally:
        await remove_client(client)
        print(f"Disconnected. Connected Clients: {len(connected_clients)}")

if __name__ == "__main__":
    model = YOLO('yolov8n.yaml').load('yolov8n.pt') # Build model and transfer weights
    
    host_name = socket.gethostname()
    ip_addresses = socket.gethostbyname_ex(host_name)
    # print(ip_addresses)

    # Print Server Address
    print(f"ws://{ip_addresses[2][-1]}:5000")

    # List to keep track of connected clients
    connected_clients = set()

    # List to keep track of emails
    notify_emails = set()

    # Start the WebSocket server
    start_server = websockets.serve(websocket_handler, ip_addresses[2][-1], 5000)

    # print("Listening to port 5000")

    # Run the server indefinitely
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
