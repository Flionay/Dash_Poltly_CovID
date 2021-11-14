from pymongo import MongoClient
from config import Config
client = MongoClient(host=Config.DATABASE_IP, port=Config.DATABASE_PORT, username=Config.DATABASE_USER, password=Config.DATABASE_PASS)

