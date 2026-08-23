import motor.motor_asyncio
import os

client= motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGO_URI","mongodb://localhost:27017"))
db=client["devportal-events"]
events_collection=db["events"]
