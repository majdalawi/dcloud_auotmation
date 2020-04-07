#!/usr/bin/env python
#Author:Ahmad Lubbad
#alubad@cisco.com
import telnetlib

import sys
import time
import datetime
import pexpect

HOST_IP = "198.18.128.96"

#### Grapping Device Info from Devices File##########
devices=open("DeviceCfg/device_list.txt","r")

##### exit_initial to handl the wizard #######
def abort_wizard(HOST_IP,port_num):
    connect_flag1=0
    connect_counter1=0
    while(connect_flag1!=1 and connect_counter1<=5):
        connect_counter1=connect_counter1+1
        try:
            telconn = pexpect.spawn("/usr/local/bin/telnet "+HOST_IP+" "+port_num)
            time.sleep(1)
            telconn.readline()
            telconn.readline()
            telconn.readline()
            telconn.sendline("\n\n")
            telconn.readline()
            index=telconn.expect(["% Please answer*","Username:","#",pexpect.EOF, pexpect.TIMEOUT])
            if index ==0:
                print (device_name+" Device is in Initial Automatic Config Mode, Exiting Now....")
                telconn.send("no\n")
                telconn.expect("% Please answer*")
                telconn.send("yes\n")
                telconn.readline()
                #print(telconn.readline())
                #print(telconn.expect(["started!",pexpect.EOF, pexpect.TIMEOUT]))
                telconn.expect("started!")
                telconn.sendline("\r\n")
                telconn.sendline("enable\n\n")
                time.sleep(.3)
                telconn.sendline("configure terminal\n\n")
                print("Initial Automatic Config  Aborted, Device is in Config Prompt")
                connect_flag1=1
                telconn.close()
                time.sleep(2)
                
            if index == 1 or index ==2:
                print ("Device is NOT in Initial Automatic Config Mode")
                connect_flag1=1
                telconn.close()
                time.sleep(2)
        except:
            print ("Connection Time Out, I will try to connect again...")
            time.sleep(2)
            if connect_counter1==5:
                print ("I tried ",connect_counter1," times but couldn't connect :-(") 
                telconn.close()
                sys.exit()
    return(True)  

start_time=datetime.datetime.now()

#### Iterate on all devices
for device in devices:
    port_num=device.split(",")[0].strip()
    device_path=device.split(",")[1].strip()
    device_name=device.split(",")[2].strip()
   
    
### Open Device Configuration File
    device_config=open(device_path,'r')

####### Call Abort Wizard Function to exit the initial configuration wizard #########
    abort_wizard(HOST_IP,port_num)
    
############ Connect To Device #####################   
    
    counter=0
    connect_flag=0
    while(connect_flag!=1 and counter<=6):
        
        try:
            connect=telnetlib.Telnet()
            counter = counter +1
            connect.open(HOST_IP,port_num)
            connect_flag=1
            print("Connected to DEVICE: "+device_name+" after",counter," attempts!!!")
            
        except:
            print ("Connection Time Out, will try to connect again...")
            time.sleep(2)
            if counter==6:
                connect.close()
                print ("I tried ",counter," times but couldn't connect :-(") 
                sys.exit()
    

    #device_log=open("device_log",'w+')
    #commands_pushed=open("commands_pushed",'w+')
    
########### Pushing Configuration Lines#################


    print("Pushing Configuration to Device: ",device_name)

    for line in device_config:
        
        connect.write(line.encode('utf-8')+b"\n")
        time.sleep(.1)
        #console = str(connect.read_very_eager())
        #device_log.write(console)
       
    connect.write(b"exit\n\n")    
    device_config.close()

    print ("finished configuring Devices: ",device_name)
    print ("Device Telnet Session Closed")
    connect.close()
    print("#############################################################################\n")
devices.close()
print("Exiting the Program Execution time is:  ",datetime.datetime.now()-start_time)
sys.exit()