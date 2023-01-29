from sqlalchemy.orm import Session

from . import models, schemas

#READ
def get_channel_id(db: Session, channel_id: int):
    return db.query(models.logChannel).filter(models.logChannel.channel_id == channel_id).first()
def get_guild_id(db: Session, guild_id: int):
    return db.query(models.logChannel).filter(models.logChannel.guild_id == guild_id).first()

#CREATE
def create_log_table(db: Session, channel_ids: schemas.logChannel):
    db_user = models.logChannel(channel_id = channel_ids.channel_id, guild_id = channel_ids.guild_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#UPDATE
def update_channel_id(db: Session, channel_ids: schemas.logChannel):
    data = db.query(models.logChannel).filter(models.logChannel.guild_id == channel_ids.guild_id).first()
    if data:
        data.channel_id = channel_ids.channel_id
        db.commit()
        db.refresh(data)
        return data
    else:
        return None