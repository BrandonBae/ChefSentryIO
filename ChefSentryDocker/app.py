from flask import Flask, request, jsonify
from serial_com import Serial
import threading
from concurrent.futures import ThreadPoolExecutor
from chefsentry_cv import CVModule
import time
import os


CV_MODULE_PERIOD = 5

temp_dict = {
    "1":"50",
    "2":"60",
    "3":"70",
    "4":"80",
    "5":"90",
}

app = Flask(__name__)

cv_module = CVModule("./resources/resnet34_07err_3classes.pkl", 1)

serial_lock = True

if (os.path.exists("/dev/ttyACM1")):
    serial = Serial("/dev/ttyACM1", 57600) 

else:
    serial = Serial("/dev/ttyACM0", 57600) 

@app.route('/zack')
def hello_zack():
    return 'Hello, Zack!'

@app.route('/rishi')
def hello_rishi():
    return 'Hello, Rishi!'

@app.route('/pajic')
def hello_pajic():
    return 'Hello, Pajic!'

@app.route('/brandon')
def hello_world():
    return 'Hello, Brandon!'

@app.route('/cooking', methods=['POST'])
def cooking():
    global serial_lock
    #print_serial()
    # Extracting JSON data from the POST request
    data = request.json
    print(data)
    # Printing the received data
    serial_res = "s "
    for temp_obj in data:
        temperature = temp_obj.get('temperature')
        time = temp_obj.get('time')
        serial_res = serial_res + f"{temperature} {60*time} "
        print(f"Temperature: {temperature}, Time: {time} min")

    while not serial_lock:
        pass

    try:
        serial_lock = False
        serial.sendToArduino(serial_res)
    finally:
        serial_lock = True

    # Responding to the client
    return jsonify(message="Data received!")

def print_serial():
    while True:
        arduinoReply = serial.recvLikeArduino()
        if not (arduinoReply == 'XXX'):
                print(f"Time {time.time()} Reply {arduinoReply}")

def run_cv_module():
    global serial_lock
    while True:
        
        prediction_res = cv_module.predict_boil()
        while not serial_lock:
            pass

        try:
            serial_lock = False
            int_res = 0
            if prediction_res == "boil":
                int_res = 2 
            if prediction_res == "simmer":
                int_res = 1
            print(f"sending prediction res {prediction_res}")
            serial.sendToArduino(f'b {int_res}')
        finally:
            serial_lock = True

        time.sleep(CV_MODULE_PERIOD)
    
"""
def play_audio():
    my_sound = pygame.mixer.Sound('sound.wav')
    my_sound.play()
    """
    
if __name__ == '__main__':
    #serial.sendToArduino("s 76 30 80 15")
    #x = threading.Thread(target=print_serial)
    #x.start()
    y = threading.Thread(target=run_cv_module)
    #z = threading.Thread(target=play_audio)
    y.start()
    # z.start()
    app.run(host='0.0.0.0', port=8080)

