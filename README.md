# YubiKey BitLocker Tool
[![forthebadge](https://forthebadge.com/images/badges/platform-windows.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/jyewman/YubiKey-Bitlocker-Tool/python-package.yml?style=for-the-badge)
![GitHub License](https://img.shields.io/github/license/jyewman/YubiKey-Bitlocker-Tool?style=for-the-badge)


## Overview
The YubiKey BitLocker Tool is a user-friendly GUI-based application that helps users manage their BitLocker TPM and PIN using a YubiKey. The tool allows users to securely set or update their BitLocker PIN by combining an 8-character alphanumeric PIN with a string generated by their YubiKey. The tool also displays the current BitLocker status and provides detailed feedback on any changes made.

---

## Table of Contents
- [Features](#Features)
- [The Release Version](#the-release-version)
- [Getting Started](#Getting-Started)
    - [Requirements](#Requirements)
    - [Installing the requirements](#installing-the-requirements)
- [License](#license)

## Features
- PIN Management: Input a user-defined 8-character alphanumeric PIN, including at least one uppercase letter and one number.
- YubiKey Integration: The tool captures the code generated by a YubiKey when pressed and concatenates it with the user's PIN to set or change the BitLocker TPM & PIN.
- BitLocker Status: Displays the current BitLocker status, including whether it is enabled or disabled.
- Logging: Detailed logs are generated to track the program’s actions and errors.
- Help & Tooltips: The tool provides in-app help and tooltips to guide users through the process.

## The Release Version
You can download the latest release from the releases page. It's just an .exe of the project. The program will automatically elevate the privileges if you don't run it as administrator.

You will need to make sure you have TPM & PIN enabled for BitLocker. There is a pretty good guide on [How To Geek](https://www.howtogeek.com/262720/how-to-enable-a-pre-boot-bitlocker-pin-on-windows/).

You will also need a YubiKey!

## Getting Started
To get this project up and running, take a look below at the requirements, you can even check out the latest release if you just want to download and go!

If you want to help out on the project, please feel free to create a pull request! You can even suggest improvements, bug fixes and anything else in the issues tracker.

### Requirements
- Python 3.8 or higher
- Pillow (Python Imaging Library) for image resizing and display
- ttkbootstrap for modern styling and theming of the GUI

### Installing the requirements
Installation is pretty simple all you need to do is install the dependencies (or just download the exe) and go!

bash:
```
pip install pillow ttkbootstrap
```

Oh, you'll also need python, and a YubiKey, but that's a given, (I hope).

## License

This tool is made available under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).
