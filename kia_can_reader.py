import cantools
import can
import time
from pprint import pprint
db = cantools.database.load_file('/home/spn/KIA_ws/hyundai_kia_generic.dbc')
### DBC file frame(arbitration) id quick list  ###
"""
902: wheel speed

"""
can_bus = can.interface.Bus(channel='can0', bitrate=500000, bustype='socketcan')
dataLogged = []
timeStart = time.time()
try:
    while True:
        message = can_bus.recv()
        if message is not None:
            try:
                message_decoded = db.decode_message(message.arbitration_id, message.data)
                # 1322: VehicleSpeed, 902: WHL_SPD
                if message.arbitration_id == 902:
                    pprint(message_decoded)
                    timeCurrent = time.time() - timeStart
                    dataLogged.append({'time': timeCurrent, 'data': message_decoded})
            except Exception as e:
                a = 0
                #print(f"Error decoding message: Unkown frame id: {e}")
except:
    pass
# except KeyboardInterrupt:
#     print("\nDo you want to save the data? (y/n): ", end="")
#     choice = input().strip().lower()
#     if choice == 'y':
#         timeSaved = time.strftime("%Y-%m-%d_%H-%M-%S")
#         fileName = f"output_{timeSaved}.txt"
#         with open(fileName, "w") as file:
#             file.write(str(dataLogged))
#         print(f"Data saved to {fileName}")
