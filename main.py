from fastapi import FastAPI, HTTPException, Depends
from typing import Union

from sql_app.database import engine, SessionLocal
from sql_app import models, schemas, crud
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/logapi/", response_model=schemas.logChannel)
def logChannelAPI(channel_ids: schemas.logChannel, db: Session = Depends(get_db)):
    data = crud.get_guild_id(db, channel_ids.guild_id)
    if data:
        raise HTTPException(status_code=409, detail="Guild ID already exists")
    return crud.create_log_table(db, channel_ids)

@app.get("/logapi/{guild_id}", response_model=schemas.logChannel)
def read_user(guild_id: int, db: Session = Depends(get_db)):
    data = crud.get_guild_id(db, guild_id)
    if data is None:
        raise HTTPException(status_code=409, detail="guild id does not exist")
    else:
        return {"guild_id": data.guild_id, "channel_id": data.channel_id}

@app.put("/logapi/", response_model=schemas.logChannel)
def update_channelId(channel_ids: schemas.logChannel, db: Session = Depends(get_db)):
    data = crud.get_guild_id(db, channel_ids.guild_id)
    if data is None:
        raise HTTPException(status_code=409, detail="guild id does not exist")
    else:
        return crud.update_channel_id(db, channel_ids)