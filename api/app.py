from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from models.data_models import CalculateRequest, CorrelationModel
from models import sql_models
from utils.stat_utils import calculate_pearson_correlation
from utils.database import SessionLocal, engine
from utils import database_communication

sql_models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    # FastAPI dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/calculate", status_code=200)
def calculate(request: CalculateRequest, db: Session = Depends(get_db)):
    pearson_correlation = calculate_pearson_correlation(request.data.x, request.data.y)
    if not pearson_correlation:
        raise HTTPException(status_code=400, detail="Couldn't calculate Pearsonr")

    database_communication.update_correlation(
        db,
        CorrelationModel(
            user_id=request.user_id,
            x_data_type=request.data.x_data_type,
            y_data_type=request.data.y_data_type,
            correlation=pearson_correlation
        )
    )


@app.get("/correlation", response_model=CorrelationModel)
def correlation(user_id: int, x_data_type: str, y_data_type: str, db: Session = Depends(get_db)):
    correlation_data = database_communication.get_correlation(db, user_id, x_data_type, y_data_type)
    if not correlation_data:
        raise HTTPException(status_code=404, detail="Couldn't find user")

    return correlation_data
