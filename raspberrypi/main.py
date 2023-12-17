# List of imports
import asyncio
import websockets
import io
from picamera2 import Picamera2
from libcamera import controls

IP_ADDRESS = "YOUR-WS-SERVER-ADDRESS"

# Initialize Camera 
picam2 = Picamera2()
picam2.start()
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous}) # Auto-Focus

async def stream():
	# Connect to the server's websocket
	async with websockets.connect(IP_ADDRESS) as websocket:
		# Upon connection send client's role/class
		await websocket.send(b"rpi")

		while True:
			# Use io.Bytes to store jpeg image in byte format
			stream = io.BytesIO()
			frame = picam2.capture_file(stream, format="jpeg")
			stream.seek(0)
			frame_data = stream.read()
			
			# Send the image to server
			await websocket.send(frame_data)

			# Reset io.Byte buffer
			stream.seek(0)
			stream.truncate()
			

			# This line is important because it prevents this client
			# to send too many frames when the server is not ready.
			# it prevents the websocket's buffer from overflowing.
			await websocket.recv() # Receive ready status from server

async def main():
	await stream()
	
if __name__ == "__main__":
	asyncio.run(main())

