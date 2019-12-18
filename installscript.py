#!/usr/bin/env python3
## Initialization, getting everything set up
import os, sys, re, io, platform, tarfile

HOME_FOLDER = os.path.expanduser("~")
CONFIG_FILES = [".bashrc", ".zshrc", ".config/fish/config.fish"]

def importDepends(package):
	global PATH_IN_CONFIG_FILE
	print("{} not found, installing package from PIP".format(package))
	os.system("pip3 install {} --user".format(package))

	## To other people and my future self: this next bit of code uses a weird hack.
	## On my PC using "with open(RC_FILE ...)" returned a "io.UnsupportedOperation:
	## not readable" error. I figured that I could do the same things while using 
	## less code using grep and pipes, as well as keep imports to their current 
	## amount. Yes, it's a hack, but it works and that's what matters.
	for file in CONFIG_FILES:
		RC_FILE = os.path.join(HOME_FOLDER, file)
		if os.path.isfile(RC_FILE):
			print("Found {}".format(RC_FILE))
			path_check = os.system("cat {} | grep 'export PATH'".format(RC_FILE))
			if path_check == 0:
				print("PATH already set in {}".format(RC_FILE))
			else:
				print("PATH set in {}".format(RC_FILE))
				os.system("echo 'export PATH={}/bin:{}/.local/bin:$PATH' >> {}".format(HOME_FOLDER, HOME_FOLDER, RC_FILE))
				os.system("source {}".format(RC_FILE))

## These are usually not installed on the system, especially new systems. This ensures they do get downloaded
try:
	import requests
except:
	importDepends("requests")
	import requests
try:	
	from bs4 import BeautifulSoup as bsoup
except:
	importDepends("bs4")
	from bs4 import BeautifulSoup as bsoup

try:
	from dialog import Dialog
except:
	importDepends("pythondialog")
	os.system("sudo apt install -y dialog")
	from dialog import Dialog

## Distributions
class debian:
	packageType = ".deb"

	def update():
		os.system("sudo apt update")
	def upgrade():
		os.system("sudo apt upgrade -y")
	def install(package):
		os.system("sudo apt install -y {}".format(package))
	def fileInstall(file):
		os.system("sudo dpkg -i {}".format(file))
		os.system("sudo apt install -f")

class ubuntu(debian):
	def addRepo(ppa):
		os.system("sudo apt-add-repository ppa:{}".format(ppa))

class fedora:
	def update():
		os.system('sudo dnf update -y')
	def install(package):
		os.system("sudo dnf install -y {}".format(package))
	def fileInstall(file):
		os.system("sudo dnf install -y {}".format(package))

class centos(fedora):
	pass

class rhel(fedora):
	pass

DISTRO = platform.dist()[0].lower()
DISTARCH = platform.machine()
print("Running on {}".format(DISTRO))
DEBIAN_BASED = ["debian", "ubuntu", "elementary"]
REDHAT_BASED = ["fedora", "rhel", "centos"]
supported = []
supported.extend(DEBIAN_BASED)
supported.extend(REDHAT_BASED)
if DISTRO not in supported:
	print("This script does not currently work on {}. Please use a supported distro or wait until your distro is supported!".format(DISTRO))
	exit()
def checkSnap():
	if not os.path.isfile("/usr/lib/snapd"):
		eval(DISTRO).install("snapd snap")
def getDeb(url, program):
	if not os.path.isdir(dl_folder):
		os.mkdir(dl_folder)

	debFile = os.path.join(dl_folder, program +".deb")

	if os.path.isfile(debFile):
		print("File {} already downloaded".format(program+".deb"))
	else:
		if "github" not in url:
			try:
				with open(debFile, "wb") as file:
					file.write(requests.get(url).contents)
			except:
				os.remove(debFile)
				os.system("wget -qO {} {}".format(debFile, url))
		elif "github" in url:
			if DISTARCH == "x86_64":
				if program == "whalebird":
					search = re.compile("x64.deb")
				else:
					search = re.compile("amd64.deb")
			pagedump = requests.get(url)
			parsedPage = bsoup(pagedump.content, 'html.parser')

			links = [a["href"] for a in parsedPage.find_all(name="a", href=search)]
			try:
				with open(debFile, "wb") as file:
					file.write(requests.get("https://github.com"+links[0]).contents)
			except:
				os.remove(debFile)
				os.system("wget -qO {} {}".format(debFile, "https://github.com"+links[0]))

	eval(DISTRO).fileInstall(debFile)
def getTar(url, program):
	if not os.path.isdir(dl_folder):
		os.mkdir(dl_folder)
	tarFile = os.path.join(dl_folder, program+".tar.xz")

	if os.path.isfile(tarFile):
		print("File {} already downloaded".format(program+".tar.xz"))
	else:
		try:
			with open(tarfile, 'wb') as file:
				file.write(requests.get(url).contents)
		except:
			os.remove(tarFile)
			os.system("wget -qO {} {}".format(tarFile, url))
	with tarfile.open(tarFile) as tar:
		tar.extractall("{}/.local/bin".format(HOME_FOLDER)

##Zenity menu
d = Dialog(dialog="dialog")
tag, options = d.checklist("DasGeek's Installer -- Re-Imagined by RiderExMachina",
					choices = 
					[("Keep Downloaded software", "", False), 
					("Testing mode", "", False),
					
					# Software repos
					#("-- TEST --"),
					("Enable Flatpak", "", False),
					("Enable SNAPS", "", False),
					
					# Notes
					("Simplenotes (SNAP)", "", False),
					
					# Social
					("Discord (Native)", "", False),
					("Discord (SNAP)", "", False),
					("Hexchat", "", False),
					("Signal (Native)", "", False),
					("Signal (SNAP)", "", False),
					("Mumble", "", False),
					("Telegram (Native)", "", False),
					("Telegram (SNAP)", "", False),
					("Whalebird (Native)", "", False),
					("Whalebird (SNAP)", "", False),
					("Wire (Native)", "", False),
					("Wire (SNAP)", "", False),
					("Zoom", "", False),
					
					# Tweaks
					("Elementary Tweaks", "", False),
					("GNOME Tweak Tool", "", False),
					("i3wm", "Dasgeek's Configuration", False),
					("Midnight Commander", "", False),
					("Ubuntu Restricted Extras", "", False),
					("XFCE Monitor Move tool", "", False),

					# Media
					("Audio Recorder", "", False),
					("Google Desktop Player (SNAP)", "", False),
					("MPV", "RiderExMachina's Configuration", False),
					("Pithos Pandora Player", "", False),
					("SMPlayer", "", False),
					("Spotify (Native)", "", False),
					("Spotify (SNAP)", "", False),

					# Internet
					("Brave", "", False),
					("Chromium (Native)", "", False),
					("Chromium (SNAP)", "", False),
					("Firefox", "", False),
					("Google Chrome", "", False),
					("Vivaldi", "", False),
					("get-iplayer (Native)", "", False),
					("get-iplayer (SNAP)", "", False),

					# A/V Editing
					("Ardour", "DAW", False),
					("Audacity", "", False),
					("ffmpeg (Native)", "", False),
					("ffmpeg (SNAP)", "", False),
					("Flowblade", "Video Editor", False),
					("Gimp (Native)", "", False),
					("Gimp (SNAP)", "", False),
					("KdenLive (AppImage)", "", False),
					("Kdenlive (Native)", "", False),
					("OBS Studio (Native)", "", False),
					("OBS Studio (SNAP)", "", False),
					("Shotwell", "", False),
					("OcenAudio", "", False),

					# Utility
					("Cheese", "Webcam Software", False),
					("Docker CE", "", False),
					("Drill (AppImage)", "File Search", False),
					("Drill (Native)", "File Search", False),
					("Etcher", "", False),
					("FISH", "BASH Alternative", False),
					("Guvcview", "Webcam settings", False),
					("Kamoso", "KDE Webcam Software", False),
					("KXStudio Jack Setup", "Advanced Audio", False),
					("Gnome-Do", "", False),
					("Synology NAS Utility", "", False),
					("Terminator", "", False),
					("Tilix", "", False),
					("VirtualBox", "", False),
					("ZSH", "BASH Alternative", False),

					# Programming and Dev
					("Android Studio", "", False),
					("Atom", "", False),
					("Filezilla", "", False),
					("Gedit", "", False),
					("Sublime Text", "", False),
					("Putty", "", False),
					("Pycharm (SNAP)", "", False),
					("Remmina", "", False),
					("VSCode", "", False),

					# Gaming & Fun
					("DOSBOX-x (SNAP)", "", False),
					("Gamehub", "", False),
					("GNOME Twitch Client", "", False),
					("Lutris", "", False),
					("Steam (Flatpak)", "", False),
					("Steam (Native)", "", False),
					("ScummVM (SNAP)", "", False),
					("AMD Padoka PPA", "", False),

					("Auto Cleanup and Update", "", True)
					],)
#print(option)
package_manager = []
snap = []
flatpak = []

dl_folder = '/tmp/ais'
for option in options:
	option = option.lower()
	
	if option == "keep downloaded software":
		pass
	if option == "testing mode":
		dl_folder = HOME_FOLDER+"/.ais"
	if option == "enable flatpak":
		eval(DISTRO).install("flatpak")
		os.system("sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo")
	if option == "enable snaps":
		eval(DISTRO).install("snap snapd")
	if option == "simplenotes (snap)":
		checkSnap()
		os.system("sudo snap install simplenotes")
	if option == "discord (native)":
		if DISTRO in DEBIAN_BASED:
			getDeb("https://discordapp.com/api/download?platform=linux&format=deb", "discord")
		else:
			print("Not yet implemented, come back later")
	if option =="discord (snap)":
		snap.append("discord")
	if option =="hexchat":
		eval(DISTRO).install("hexchat")
	if option =="signal (native)":
		if DISTRO in DEBIAN_BASED:
			os.system("wget -qO - https://updates.signal.org/desktop/apt/keys.asc | sudo apt-key add -")
			os.system('echo "deb [arch=amd64] https://updates.signal.org/desktop/apt xenial main" | sudo tee -a /etc/apt/sources.list.d/signal-xenial.list')
			debian.update()
			debian.install("signal-desktop")
		else:
			print("Signal does not have a package for your system. Installing the SNAP version")
			snap.append("signal-desktop")
	if option =="signal (snap)":
		snap.append("signal-desktop")
	if option =="mumble":
		eval(DISTRO).install("mumble")
	if option =="telegram (native)":
		getTar("https://telegram.org/dl/desktop/linux", "telegram")
	if option =="telegram (snap)":
		snap.append("telegram-desktop")
	if option =="whalebird (native)":
		if DISTRO in DEBIAN_BASED:
			getDeb("https://github.com/h3poteto/whalebird-desktop/latest", "whalebird")
		else:
			print("Not yet implemented, come back later")
	if option =="whalebird (snap)":
		snap.append("whalebird")
	# if option =="wire (native)":
	if option =="wire (snap)":
		snap.append("wire")
	# if option =="zoom":
	# if option =="elementary tweaks":
	# if option =="gnome tweak tool":
	# if option =="i3wm":
	# if option =="midnight commander":
	# if option =="ubuntu restricted extras":
	# if option =="xfce monitor move tool":
	# if option =="audio recorder":
	if option =="google desktop player (snap)":
		snap.append("google-play-music-desktop-player")
	# if option =="mpv":
	# if option =="pithos pandora player":
	# if option =="smplayer":
	# if option =="spotify (native)":
	if option =="spotify (snap)":
		snap.append("spotify")
	# if option =="brave":
	# if option =="chromium (native)":
	if option =="chromium (snap)":
		snap.append("chromium")
	# if option =="firefox":
	# if option =="google chrome":
	# if option =="vivaldi":
	# if option =="get-iplayer (native)":
	if option =="get-iplayer (snap)":
		snap.append("get-iplayer")
	# if option =="ardour":
	# if option =="audacity":
	# if option =="ffmpeg (native)":
	if option =="ffmpeg (snap)":
		os.system("sudo snap install ffmpeg --classic")
	# if option =="flowblade":
	# if option =="gimp (native)":
	if option =="gimp (snap)":
		os.system("sudo snap install gimp --edge")
	# if option =="kdenlive (appimage)":
	# if option =="kdenlive (native)":
	# if option =="obs studio (native)":
	if option =="obs studio (snap)":
		snap.append("obs-studio")
	# if option =="shotwell":
	# if option =="ocenaudio":
	# if option =="cheese":
	# if option =="docker ce":
	# if option =="drill (appimage)":
	# if option =="drill (native)":
	# if option =="etcher":
	# if option =="fish":
	# if option =="guvcview":
	# if option =="kamoso":
	# if option =="kxstudio jack setup":
	# if option =="gnome-do":
	# if option =="synology nas utility":
	# if option =="terminator":
	# if option =="tilix":
	# if option =="virtualbox":
	# if option =="zsh":
	# if option =="android studio":
	# if option =="atom":
	# if option =="filezilla":
	# if option =="gedit":
	# if option =="sublime text":
	# if option =="putty":
	if option =="pycharm (snap)":
		snap.append("pycharm")
	# if option =="remmina":
	# if option =="vscode":
	if option =="dosbox-x (snap)":
		snap.append("dosbox-x")
	# if option =="gamehub":
	# if option =="gnome twitch client":
	# if option =="lutris":
	# if option =="steam (flatpak)":
	# if option =="steam (native)":
	if option =="scummvm (snap)":
		snap.append("scummvm")
	# if option =="amd padoka ppa":
	# if option =="auto cleanup and update":

if len(flatpak) > 0:
	print("This is no yet implemented. Please try again later!")
if len(package_manager) > 0:
	eval(DISTRO).install(" ".join(package_manager))
if len(snap) > 0:
		os.system("sudo snap install {}".format(" ".join(snap)))