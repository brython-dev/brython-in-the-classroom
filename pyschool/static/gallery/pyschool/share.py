print("this script demonstrates the use of shared modules in pyschool.net")

import sys

# add path of shared module, 

# this "path" was created by creating a greeting.py module saved as "/libs/greeting.py".
# we then click on menu (3 vertical bars), then selected share/unshare.
# this displays a File List dialog, click on the "share" checkbox next to libs.
# a shareID value will populate the shareID column for libs.  Click on the libs entry
# and a path such as "/Shares/fa3098c5a2f22a89e3b0ad8217f02552" is displayed.

sys.path.append("/Shares/fa3098c5a2f22a89e3b0ad8217f02552")  

import greeting    #greeting.py is a user defined module, that has been shared by the owner

greeting.greeting("hello world!")
