import cantools
import can
import time
from pprint import pprint
import usb

### DBC file frame(arbitration) id quick list  ###
""" KIA: hyundai_kia_generic.dbc
902: wheel speed
881: Brake/Acc Position // brake>15 brakelight on.
916: BrakeLight // not working
1322: VehicleSpeed
544: acceleration
"""

""" Corolla: toyota_new_mc_pt_generated.dbc
37: Steering
548: Brake
"""

# Specify your system here
currentSystem = "Windows"

if currentSystem == "Windows":
    # db = cantools.database.load_file('C:/Users/xuanp/OneDrive - email.ucr.edu/Study/Cecert/KIA-CAN/hyundai_kia_generic.dbc')
    db = cantools.database.load_file('C:/Users/xuanp/OneDrive - email.ucr.edu/Study/Cecert/KIA-CAN/toyota_new_mc_pt_generated.dbc')

    # Find the USB device
    # 0x1D50, 0x606F 
    try:
        # Find the USB device
        # 0x1D50, 0x606F 
        # dev = usb.core.find(idVendor=0x0403, idProduct=0xFFA8)
        dev = usb.core.find(idVendor=0x1D50, idProduct=0x606F)
        if dev is None:
            raise ValueError("USB2CAN Device not found")

        # Initialize the CAN bus
        # bus = can.Bus(interface='gs_usb', channel=dev.product, bus=dev.bus, address=dev.address, bitrate=500000)
        bus = can.Bus(interface='gs_usb', channel=dev.product, bus=dev.bus, address=dev.address, bitrate=500000)
        print(f"CAN adapter initialized: {bus}")
    
    except can.CanError as e:
        print(f"Failed to initialize CAN adapter: {e}")
    
    dataLogged = []
    timeStart = time.time()

    BRAKE_PRESSURE = []
    try:
        while True:
            message = bus.recv()
            # print(message)
            if message is not None:
                try:
                    message_decoded = db.decode_message(message.arbitration_id, message.data)
                    # print(type(message.arbitration_id))
                    # print(message_decoded)
                    
                    # 1322: VehicleSpeed, 902: WHL_SPD 37, 643, 
                    if message.arbitration_id in [548]:
                        timeCurrent = time.time() - timeStart
                        print(f'\r[{timeCurrent}] {message_decoded}', end='', flush=True)

                        BRAKE_PRESSURE.append(message_decoded["BRAKE_PRESSURE"])
                        print(max(BRAKE_PRESSURE))
                        # dataLogged.append({'time': timeCurrent, 'data': message_decoded})
                except Exception as e:
                    a = 0
                    #print(f"Error decoding message: Unkown frame id: {e}")
    except:
        pass
    # except KeyboardInterrupt:
    #     print("/nDo you want to save the data? (y/n): ", end="")
    #     choice = input().strip().lower()
    #     if choice == 'y':
    #         timeSaved = time.strftime("%Y-%m-%d_%H-%M-%S")
    #         fileName = f"output_{timeSaved}.txt"
    #         with open(fileName, "w") as file:
    #             file.write(str(dataLogged))
    #         print(f"Data saved to {fileName}")

if currentSystem == "Linux":
    db = cantools.database.load_file('/home/spn/KIA_ws/hyundai_kia_generic.dbc')
    ### DBC file frame(arbitration) id quick list  ###
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
