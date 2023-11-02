# import required libraries
import cv2
from human_detector import detect_humans
from camera import Camera
import asyncio
import websockets
from time import sleep

# create handler for each connection

image_path = "./resources/images/cooker.jpg"
camera_module = Camera()
async def handler(websocket, path):

    while True:
        sleep(10)
        data = await websocket.recv()
        ## Here we should take picture using camera module for now manually load image from resource folder
        Camera.take_picture(image_path)
        num_humans = detect_humans(image_path)
        reply = f"Data recieved as:  {data}! Number of Humans Detected: {num_humans}"
        await websocket.send(reply)


start_server = websockets.serve(handler, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()