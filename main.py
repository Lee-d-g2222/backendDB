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

#SET LOG CHANNEL
@app.post("/logchannel/set", response_model=schemas.logChannel)
def set_log_channel(jSON: schemas.logChannel, db: Session = Depends(get_db)):
    data = crud.get_guild_id(db, jSON.guild_id)
    # if db is not empty -> create new
    if data is None:
        check = crud.create_log_table(db, jSON)
        if check is None:
            raise HTTPException(status_code=409, detail="dbCreateFailed")
        else:
            raise HTTPException(status_code=201, detail="dbCreateSuccess")
        
    # if channel id is same -> do nothing
    elif data.channel_id == jSON.channel_id:
        raise HTTPException(status_code=409, detail="sameChannelId")
    
    # if channel id is not same -> update
    else:
        check = crud.update_channel_id(db, jSON)
        if check is None:
            raise HTTPException(status_code=409, detail="dbUpdateFailed")
        else:
            raise HTTPException(status_code=201, detail="dbUpdateSuccess")

#GET LOG CHANNEL ID
@app.get("/logchannel/get/{guild_id}", response_model=Union[schemas.logChannel, None])
def get_channel_id(guild_id: str, db: Session = Depends(get_db)):
    data = crud.get_guild_id(db, guild_id)
    if data is None:
        raise HTTPException(status_code=404, detail="dbNotFound")
    else:
        return data