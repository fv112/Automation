import ast
import ctypes
import datetime
import hashlib
import io
import json
import os
import os.path
import pyautogui                                        # Press keyboard outside the browser.
import pyscreenshot as pyscreenshot
import pythoncom
import random
import re as regex
import requests
import shutil
import socket
import subprocess
import sys
import time
import urllib3
import win32api                                         # Read the Windows login.
import win32com.client as win
import win32net                                         # Read the Windows login.
import yaml
import zipfile
import pyscreenshot as pyscreenshot
from bs4 import BeautifulSoup
from collections import Counter
from deep_translator import GoogleTranslator
from docx import Document
from docx.shared import Inches
from docx.shared import RGBColor
from faker import Faker
from jsonschema import validate, ValidationError
from pathlib import Path
from PIL import ImageGrab
from prettytable import PrettyTable
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

sys.path.insert(0, os.path.abspath('./Automations/modules'))
import automationAux as Aux
import connections as Con
import automationFunc as Func
import automationCore as Core
