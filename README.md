Author: Ahmad Lubbad 
alubad@cisco.com

This is a python3 script to automate initial configuration of Cisco dCluod CSS lab, the script will exit  the initial automatic installation wizard and push configuration from the configuration files under "DeviceCfg" directory
you need to be connected to the dCloud VPN
Devices configured are listed in the device_list file in the following format starting with port number, configuration file path, device name, below is an example:

2023,DeviceCfg/Core.txt,Core

The following devices are listed in the deivce_list file by default however more devices can be added:

-Fusion
-Core
-Edge-1
-Edge-2 
© 2020 GitHub, Inc.
