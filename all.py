import socket
from tcp_by_size import recv_one_message, send_one_message
import threading
from tkinter import *
import os,string,time, glob
from ctypes import windll
import shutil
from cryptography.fernet import Fernet