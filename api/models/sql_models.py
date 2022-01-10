from sqlalchemy import Column, Integer, String, Float

from utils.database import Base


class UserCorrelation(Base):
    __tablename__ = "correlations"

    user_id = Column(Integer, primary_key=True, index=True)
    x_data_type = Column(String, primary_key=True, index=True)
    y_data_type = Column(String, primary_key=True, index=True)
    value = Column(Float)
    p_value = Column(Float)
