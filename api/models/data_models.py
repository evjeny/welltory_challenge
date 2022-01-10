import datetime

from pydantic import BaseModel


class DateStatModel(BaseModel):
    date: datetime.date
    value: float


class ObservationsModel(BaseModel):
    x_data_type: str
    y_data_type: str
    x: list[DateStatModel]
    y: list[DateStatModel]


class CalculateRequest(BaseModel):
    user_id: int
    data: ObservationsModel


class PearsonCorrelationModel(BaseModel):
    value: float
    p_value: float


class CorrelationModel(BaseModel):
    user_id: int
    x_data_type: str
    y_data_type: str
    correlation: PearsonCorrelationModel
