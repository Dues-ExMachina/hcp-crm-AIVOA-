from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from core.database import Base
from models.hcp import HCP  
class Interaction(Base):
    __tablename__ = "interactions"

    id                      = Column(Integer, primary_key=True, autoincrement=True)
    hcp_id                  = Column(Integer, ForeignKey("hcps.id", ondelete="SET NULL"), nullable=True)
    rep_id                  = Column(Integer, nullable=False, default=1)
    interaction_type        = Column(Enum("Meeting", "Call", "Email", "Conference"), default="Meeting")
    interaction_date        = Column(Date, nullable=False)
    interaction_time        = Column(Time, nullable=True)
    attendees               = Column(Text)
    topics_discussed        = Column(Text)
    materials_shared        = Column(Text)
    samples_distributed     = Column(Text)
    sentiment               = Column(Enum("Positive", "Neutral", "Negative"), default="Neutral")
    outcomes                = Column(Text)
    follow_up_actions       = Column(Text)
    ai_summary              = Column(Text)
    ai_suggested_followups  = Column(Text)
    raw_chat_input          = Column(Text)
    created_at              = Column(DateTime, server_default=func.now())
    updated_at              = Column(DateTime, server_default=func.now(), onupdate=func.now())
