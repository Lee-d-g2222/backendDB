from pydantic import BaseModel

class logChannelBase(BaseModel):
    channel_id: str
    guild_id: str

class logChannel(logChannelBase):
    class Config:
        orm_mode = True
