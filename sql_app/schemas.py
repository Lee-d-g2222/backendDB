from pydantic import BaseModel

class logChannelBase(BaseModel):
    channel_id: int
    guild_id: int

class logChannel(logChannelBase):
    class Config:
        orm_mode = True
