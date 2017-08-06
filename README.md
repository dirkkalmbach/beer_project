
*This Project is part of the [Udacity Full Stack Web Devoloper Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).* It consists of an application which provides a list of items within a variety of beer categories as well as a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

# How to run
## Prerequisite: Install the Vagrant VM
To open and modify this application, you need to run a web server and a web app that uses it: *Vagrant Virtual Machine* The Vagrant VM is a Linux system that runs on top of your own machine. For this you have to download and install VirtualBox and Vagrant:

### VirtualBox
*VirtualBox* is the software that actually runs the VM. [You can download it from virtualbox.org, here](https://www.virtualbox.org/wiki/Downloads). Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it.

*Ubuntu 14.04 Note: If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center, not the virtualbox.org web site. Due to a reported [bug](https://ubuntuforums.org/showthread.php?t=2227131), installing VirtualBox from the site may uninstall other software you need.*

### Vagrant
*Vagrant* is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. [You can download it from vagrantup.com.](https://www.vagrantup.com/downloads.html) Install the version for your operating system.

*Windows Note: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.*

## Run the App
1. Clone or download this repository
2. Run the VM: using the terminal, change directory to */beer_project* using the command `cd <path to beer_project/vagrant>` (the folder with *vagrant* file), then type `vagrant up` to launch your virtual machine.
3. Running the App: type `vagrant ssh` to log into your VM (if you want to exit the VM, type `exit`). Type `cd /vagrant` and run the app by typing `python3 application.py` in the terminal console. 
4. Go to [localhost:8000](http://localhost:8000) and enjoy :-)

# What can I do with it?
You can use the application for your own purpose, e.g.:

- Alter the code *database_setup.py* to create your own catalog-item-project. The database consists of 3 Tables: *category, item, user* with the corresponding Classes *Category, Item, User* in *database_setup.py*.

- Alter the code in *application.py*. This is the main file server-side connecting to the database and rendering the html-sites client-side.

- Alter the html-sites in */templates* to change the the look&feel of the website.

The Folder structure looks like this:

beer_project/    
├── vagrant/   
│   ├── application.py   
│   ├── database_setup.py     
│   ├── database_filling.py *(initial filling the db with entries)*   
│   ├── beermenuwithusers.db *(created afterrunning database_setup.py)*    
│   ├── client_secret.json *(for Google oAuth)*  
│   ├── templates/  
│   │    ├── index.html *(logged in)*  
│   │    ├── publicindex.html *(not logged in)*  
│   │    ├── catalog.html *(renders depending on login-status)*  
│   │    ├── item.html *(renders depending on login-status)*  
│   │    ├── login.html  
│   │    ├── additem.html *(logged in)*  
│   │    ├── edititem.html *(logged in)*  
│   │    ├── deleteitem.html *(logged in)*  
│   │    ├── main.html *(<head> element for all other html-sites)*  
│   │    ├── header.html *(html-elements for logged-in sites)*  
│   │    └── publicheader.html *(html-elements for public sites)*  
│   ├── static/  
│   │    └── styles.css  
│   └── vagrantfile *(contains the Vagrant VM data)*  
└── README.md *(this file)*  


# References

- [Udacity Course: Full Stack Foundations](https://www.udacity.com/course/full-stack-foundations--ud088)

- [Udacity Course: Authentication & Authorization](https://www.udacity.com/course/authentication-authorization-oauth--ud330)

- [Beer types as inital database entries](http://www.thebeerstore.ca/beer-101/beer-types)

