#
# Copyright 2025 Lorenzo Maiuri
# Published under GPL-3.0 license
# GitHub : https://github.com/H3rz3n/davinci-helper
#

#-----------------------------------------------------------------------------------------------------

# STANDARD MODULES IMPORT
from pathlib import Path
import sys, os, subprocess, threading, gettext, locale, re

#-----------------------------------------------------------------------------------------------------

# DEFINING UI FILES PATH
ui_path = os.path.join("/usr/share/davinci-helper/data/ui")

# DEFINING ICON FILES PATH
icon_path = os.path.join("/usr/share/davinci-helper/data/icons")

# DEFINING TRANSLATE FILES PATH
locale_path = os.path.join("/usr/share/davinci-helper/locale")

#-----------------------------------------------------------------------------------------------------

# ASSOCIATE THE NAME OF THE TRANSLATION DICTIONARY TO THIS FILE PATH FOR THE LOCALE MODULE
locale.bindtextdomain('davinci-helper', locale_path)

# ASSOCIATE THE NAME OF TRANSLATION DICTIONARY TO THIS FILE PATH FOR THE GETTEXT MODULE
gettext.bindtextdomain('davinci-helper', locale_path)

# TELLING GETTEXT WHICH FILE TO USE FOR THE TRANSLATION OF THE APP
gettext.textdomain('davinci-helper')

# TELLING GETTEXT THE TRANSLATE SIGNAL
_ = gettext.gettext

#-----------------------------------------------------------------------------------------------------

# FUNCTION THAT CHECK WHICH VERSION OF FEDORA IS INSTALLED
def check_fedora_version () -> str:
    os_version = None
    os_release_path = Path("/etc/os-release")

    try:
        # For Fedora, Nobara and Ultramarine Linux we can
        # use a simple OS version detection:
        # we simply read /etc/os-release, which is formatted like this:
        # NAME="Fedora Linux"
        # VERSION="43 (Workstation Edition)"
        # RELEASE_TYPE=stable
        # ID=fedora
        # VERSION_ID=43
        # [..other stuff..]
        os_release_text = os_release_path.read_text()
        os_name = re.findall(r'^NAME="([a-zA-Z" ]+)"', os_release_text)[0]

        if os_name in ["Fedora Linux", "Nobara Linux", "Ultramarine Linux"]:
            version_num = re.findall(rf'VERSION_ID=(\d+)', os_release_text)
            version_num = int(version_num[0])
            os_version = f"{os_name} {version_num}"

        else:
            os_info = subprocess.run("hostnamectl", capture_output=True, text=True)
            if ((os_info.stdout).lower()).find("rawhide") != -1 :
                os_version = "Fedora Linux Rawhide"

        if not os_version:
            raise RuntimeError("Could not detect OS version in use!")

        print(f"You are using a supported OS version : {os_version}")
        return os_version

    except Exception as err:
        print(_("DEBUG : There was an error reading what OS is installed :"))
        print(f"Error: {err}")
        print("")
        os_info = locals().get('os_info')
        if os_info:
            print(os_info.stderr)
            print("")
        print(_("Please open an issue report and paste this error code on the project GitHub page :"))
        print("https://github.com/H3rz3n/davinci-helper/issues\n")
        exit(1)

    #-----------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------

# FUNCTION THAT ADDS THE RPM FUSION REPOSITORY
def add_repository():

    #-----------------------------------------------------------------------------------------------------

    # ACQUIRING IF RPM FUSION REPO IS ALREADY INSTALLED
    rpm_fusion_repo_check = subprocess.run("dnf repolist", shell=True, capture_output=True, text=True )

    # CHECKING IF RPM FUSION REPO IS ALREADY INSTALLED
    if rpm_fusion_repo_check.stdout.find("rpmfusion-free") != -1 and rpm_fusion_repo_check.stdout.find("rpmfusion-nonfree"):

        # PRINTING THE MESSAGE
        print(_("The RPM Fusion repository had already been added to the system, there was no need to add it."))
        print("")

    else :
    
        # ADDING THE RPM FUSION REPOSITORY
        adding_repo = subprocess.run("dnf install -y https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm", shell=True, capture_output=True, text=True )

        # CHECKING IF THERE WERE ERRORS
        if adding_repo.returncode != 0 :

            # PRINTING THE ERROR MESSAGE
            print(_("DEBUG : It was impossible to add the RPM Fusion Free and Non-Free repository."))
            print(_("Check your network connection and try again or add it by yourself."))
            print("")
            print(adding_repo.stdout)
            print("")
            print(_("Please open an issue report and paste this error code on the project GitHub page :"))
            print("")
            print("https://github.com/H3rz3n/davinci-helper/issues")
            print("")
            exit(2)

        else :

            # PRINTING THE SUCCESSFUL STATE
            print(_("The RPM Fusion Free and Non-Free repository have been successfully added."))
            print("")

    #-----------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------
























