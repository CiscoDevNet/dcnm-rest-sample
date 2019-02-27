# Data Center Network Management REST Sample

This is a collection of sample REST API client code for Cisco Data Center Network Manager (DCNM).
For DCNM software download and documentation, please refer to [http://www.cisco.com/go/dcnm](http://www.cisco.com/go/dcnm)

## Prerequisites	
Tested with Python3.6.4 and DCNM 10.3(1),10.4(1),10.4(2) and 11.0(1) 

## Sample Code

* manageLanSwitch.py: sample code to change device management state

* deleteLanSwitch.py: sample code to delete an ethernet switch from DCNM

* discoverLanSwitch.py: sample code to discover ethernet switch 

* discoverSanFabric.py: sample code to discover FC/San fabric

* getSwitchCPU.py: sample code to retrieve CPU chart for a specific switch

* getAllAlarm.py: sample code to retrieve all outstanding alarms and associated events
 
* getAllEtherInterfaceStats.py: sample code to retrieve all Ether interface stats

* getAllFCInterfaceStats.py: sample code to retrieve all FC interface stats

* getFCInterfaceStats.py: sample code to retrive switch FC interface statistics

* getSwitchCPU.py: Sample code to retrieve FC/SAN switch CPU utilization.

* getLanSwitchCPU.py: Sample code to retrieve Ethernet/LAN switch CPU utilization.

* getLanSwitchMem.py: Sample code to retrieve Ethernet/LAN switch Memory utilization.

* manageUser.py: Sample code to change local user password

* getServerStatus.py: Sample code to get DCNM server running status
 
* sanZoningSample.py: Sample code to create zone for init/target pair, activate zonset for fabric running enhanced zone mode.
