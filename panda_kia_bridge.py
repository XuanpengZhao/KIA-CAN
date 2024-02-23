#!/usr/bin/env python3
from panda import Panda
import can, cantools
#import sys
#sys.path.append('/path/to/openpilot')  # Replace with the actual path to the openpilot directory
from opendbc.can.packer import CANPacker
from openpilot.selfdrive.car.hyundai import hyundaican
from openpilot.selfdrive.car.hyundai.values import CAR
import cereal.messaging as messaging

db = cantools.database.load_file('hyundai_kia_generic.dbc')
dbc_file = "hyundai_kia_generic"
# Init panda
p = Panda()

# Set safety mode to allow everything
p.set_safety_mode(p.SAFETY_ALLOUTPUT)

def cullControl(packer, frame, button):
    clu11 = {
        "CF_Clu_CruiseSwState": 0,
        "CF_Clu_CruiseSwMain": 0,
        "CF_Clu_SldMainSW": 0,
        "CF_Clu_ParityBit1": 1,
        "CF_Clu_VanzDecimal": 0,
        "CF_Clu_Vanz": 0,
        "CF_Clu_SPEED_UNIT": 1,
        "CF_Clu_DetentOut": 0,
        "CF_Clu_RheostatLevel": 1,
        "CF_Clu_CluInfo": 0,
        "CF_Clu_AmpInfo": 0,
        "CF_Clu_AliveCnt1": 0}
    car_fingerprint = CAR.KIA_NIRO_EV # KIA_NIRO_EV
    return hyundaican.create_clu11(packer, frame, clu11, button, car_fingerprint)
      

def steeringControl(packer, frame, steer_req):
     

            # Define the function arguments (replace with actual values)
    # frame = 0 # 0~15
    car_fingerprint = CAR.KIA_NIRO_EV # KIA_NIRO_EV
    apply_steer = steer_req 
    steer_req = 1
    
    
    # steer_req = 0   
    torque_fault = False
    lkas11 = {
            "CF_Lkas_LdwsActivemode": 0,
            "CF_Lkas_LdwsSysState": 1,
            "CF_Lkas_SysWarning": 0,
            "CF_Lkas_LdwsLHWarning": 0,
            "CF_Lkas_LdwsRHWarning": 0,
            "CF_Lkas_HbaLamp": 0,
            "CF_Lkas_FcwBasReq": 0,
            "CF_Lkas_HbaSysState": 0,
            "CF_Lkas_FcwOpt": 0,
            "CF_Lkas_HbaOpt": 1,
            "CF_Lkas_FcwSysState": 0,
            "CF_Lkas_FcwCollisionWarning": 0,
            "CF_Lkas_FusionState": 0,
            "CF_Lkas_FcwOpt_USM": 1,
            "CF_Lkas_LdwsOpt_USM": 1} 
    sys_warning = False  
    sys_state = 1
    enabled = False   
    left_lane = 0   
    right_lane = 0   
    left_lane_depart = 0   
    right_lane_depart = 0   
 
    # print("apply_steer: ", apply_steer)
    # print("steer_req: ", steer_req)
    # Call the create_lkas11 function
    return hyundaican.create_lkas11(packer, frame, car_fingerprint, apply_steer, steer_req,
                            torque_fault, lkas11, sys_warning, sys_state, enabled,
                            left_lane, right_lane, left_lane_depart, right_lane_depart)
  

def lfahdaControl(packer, ifLF, speed):
    return hyundaican.create_lfahda_mfc(packer, ifLF, speed)

def accControl(packer, enabled, accel, idx, set_speed, stopping, long_override, use_fca):
    upper_jerk = 0.3
    lead_visible = 0
    return hyundaican.create_acc_commands(packer, enabled, accel, upper_jerk, idx, lead_visible, set_speed, stopping, long_override, use_fca)

frame = {
    "LKAS11": 0,
    "CLU11": 0,
    "SCC11": 0,
    "SCC12": 0,
    "SCC14": 0,
    "FCA11": 0
}
steer_req = 0   
steer_req_last = 0
joystickSocket = messaging.sub_sock('testJoystick')
packer = CANPacker(dbc_file)

enabled = True
accel = 0.3
set_speed = 26
stopping = False
long_override = False
use_fca = True

#try:
while True:
    msgs = p.can_recv()
    # can id, whatever, data, bus number
    # bus 0 = car, bus 2 = camera
    mailbox = []
    

    for canid, whatever, data, source in msgs:
            
        # if canid in [1056, 1057, 905, 909] and source == 0:  # 1056: SCC11, 1057: SCC12, 905: SCC14, 1265: CLU11
        #                     #, 909: FCA11, 1157: LFAHDA
        # #    print("source: ", source) # can: 130???
        #     print("canid: ", canid)
        #     decoded = db.decode_message(canid, data)
        #     print(decoded)

        # From car to camera
        if(source == 0):
            # if (canid == 1056):
            #     mailbox.append(accControl(packer, enabled, accel, frame["SCC11"], set_speed, stopping, long_override, use_fca)[0])
            #     frame["SCC11"] += 1
            #     continue
            # if (canid == 1057):
            #     mailbox.append(accControl(packer, enabled, accel, frame["SCC12"], set_speed, stopping, long_override, use_fca)[1])
            #     frame["SCC12"] += 1
            #     continue
            # if (canid == 905):
            #     mailbox.append(accControl(packer, enabled, accel, frame["SCC14"], set_speed, stopping, long_override, use_fca)[2])
            #     frame["SCC14"] += 1
            #     continue
            # if (canid == 909):
            #     mailbox.append(accControl(packer, enabled, accel, frame["FCA11"], set_speed, stopping, long_override, use_fca)[3])
            #     frame["FCA11"] += 1
            #     continue
           
            # 1265: CLU11
            # if (canid == 1265):
            #     botton = 1
            #     mailbox.append(packer, cullControl(frame["CLU11"], botton))
            #     frame["CLU11"] += 1
            #     continue
            mailbox.append((canid, whatever, data, 2))
            

        # From camera to car (we're more interested in this)
        elif(source == 2):
            
            # # 1157: LFAHDA
            # if (canid == 1157):
            #     ifLF = True
            #     speed = 24
            #     mailbox.append(lfahdaControl(packer, ifLF, speed))
            #     continue

            # 832: LKAS11, 
            if(canid == 832):
                msg = messaging.recv_sock(joystickSocket)
                if msg is not None:
                    steer_req = msg._get("testJoystick")._get("axes")[1] # -1~1
                    steer_req *= 1024
                mailbox.append(steeringControl(packer, frame["LKAS11"], steer_req))
                frame["LKAS11"] += 1
                continue
       
            mailbox.append((canid, whatever, data, 0))
        
    p.can_send_many(mailbox)


# except KeyboardInterrupt:
#     createdLKAS11, frame, steer_req = steeringControl(frame, 0)
#     mailbox.append((canid, whatever, createdLKAS11[2], 0))
#     p.can_send_many(mailbox)

