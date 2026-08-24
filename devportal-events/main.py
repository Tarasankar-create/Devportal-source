from fastapi import FastAPI
from models import JenkinsEvent,ArgoCDEvent
from db import events_collection
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/webhooks/jenkins")
async def jenkisn_webhook(event: JenkinsEvent):
    doc=event.model_dump()
    doc["source"]="jenkins"
    await events_collection.insert_one(doc)
    return {"Status": "Received"}

@app.post("/webhooks/argocd")
async def argocd_webhook(event: ArgoCDEvent):
    doc=event.model_dump()
    doc["source"]="argocd"
    await events_collection.insertone(doc)
    return {"status": "Received"}

@app.get("/events")
async def get_events(limit: int=50):
    cursor=events_collection.find().sort("timestamp",-1).limit(limit)
    result=[]
    async for doc in cursor:
        doc["_id"]=str(doc["_id"])
        result.append(doc)
    return result