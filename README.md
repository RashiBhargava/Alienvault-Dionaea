Alienvault-Dionaea
==================

This project provides some basic integration between Dionaea (via the HoneyDrive project, http://bruteforce.gr/honeydrive) and Alienvault's OSSIM (http://www.alienvault.com/). 

*alienvault directory*

* 00-dionaealog.conf: Drop in to /etc/rsyslog.d to parse out the dionaealog data source. 

* dionaealog.cfg: This data source needs to be copied to /etc/ossim/agent/plugins. Once this is complete enable (via the command line or GUI) and you should be able to see Dionaea events. 

* dionaealog.sql: A SQL config file that defines the data source. The ID is 9902, you will want to double check this isn't in use in your environment. Tip - by default the priority and reliability of event 99 is intended to raise an alarm. If you are using correlation directives to manage the Dionaea events you may want to set this to a lower value. 


*honeydrive directory*

* 30-dionaea.conf: After the data is flowing to syslog it needs to be exported from the honeydrive server to your Alienvault instance. This file sets up syslog forwarding for the application named dionaealog.py to an outside host via UDP. 

* dionaealog.py: This file periodically reads from the locally maintained sqlite database for dionaea. It was modified slightly for outputting to syslog. The original release of this script was shamelessly copied from DionaeaOSSIM on Github and modified to this project's needs. 

* rc.local: This script automatically starts Dionaea and the associated export script. Save to /etc/rc.local to use. 
