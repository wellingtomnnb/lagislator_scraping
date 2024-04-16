# pip install motor
from motor import motor_asyncio

class Database:

    def __init__(self):
        user, passwd = "root", "scraping"
        MONGO_DETAILS = f"mongodb://{user}:{passwd}@localhost:27017"

        client = motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
        database = client['legislator']

        self.preposicoes = database.get_collection("preposicoes")