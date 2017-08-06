
# How to run
## Prereqresite: Install the Vagrant VM
To open and modify this application, you need to run a web server and a web app that uses it. The Vagrant VM is a Linux system that runs on top of your own machine. For this you have to download and install VirtualBox and Vagrant:

###VirtualBox
VirtualBox is the software that actually runs the VM. [You can download it from virtualbox.org, here](https://www.virtualbox.org/wiki/Downloads). Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it.

*Ubuntu 14.04 Note: If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center, not the virtualbox.org web site. Due to a reported [bug](https://ubuntuforums.org/showthread.php?t=2227131), installing VirtualBox from the site may uninstall other software you need.*

###Vagrant
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. [You can download it from vagrantup.com.](https://www.vagrantup.com/downloads.html) Install the version for your operating system.

*Windows Note: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.*

## Run the App
1. Clone or download this repository
2. Run the VM: using the terminal, change directory to beer_project using the command `cd <path to beer_project>`, then type `vagrant up` to launch your virtual machine.
3. Running the App: type `vagrant ssh` to log into your VM (if you want to exit the VM, type `exit`). Now run the app by typing `python3 application.py`. Go to [localhost:8000](localhost:8000) and enjoy :-)

# What can I do with it?

...



# References

- [Udacity Course: Full Stack Foundations](https://www.udacity.com/course/full-stack-foundations--ud088)

- [Udacity Course: Authentication & Authorization](https://www.udacity.com/course/authentication-authorization-oauth--ud330)

- [Beer types as inital database entries](http://www.thebeerstore.ca/beer-101/beer-types)

