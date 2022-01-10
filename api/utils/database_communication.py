from sqlalchemy import sql
from sqlalchemy.orm import Session

from models import sql_models, data_models


def update_correlation(
    db: Session,
    user_correlation: data_models.CorrelationModel
):
    db_correlation = db.query(sql_models.UserCorrelation).filter(
        sql_models.UserCorrelation.user_id == user_correlation.user_id,
        sql_models.UserCorrelation.x_data_type == user_correlation.x_data_type,
        sql_models.UserCorrelation.y_data_type == user_correlation.y_data_type
    ).first()

    if db_correlation:
        db_correlation.value = user_correlation.correlation.value
        db_correlation.p_value = user_correlation.correlation.p_value
    else:
        db_correlation = sql_models.UserCorrelation(
            user_id=user_correlation.user_id,
            x_data_type=user_correlation.x_data_type,
            y_data_type=user_correlation.y_data_type,
            value=user_correlation.correlation.value,
            p_value=user_correlation.correlation.p_value
        )
        db.add(db_correlation)

    db.commit()


def get_correlation(
    db: Session, user_id: int,
    x_data_type: str,
    y_data_type: str
) -> data_models.CorrelationModel | None:
    db_correlation = db.query(sql_models.UserCorrelation).filter(
        sql_models.UserCorrelation.user_id == user_id,
        sql_models.UserCorrelation.x_data_type == x_data_type,
        sql_models.UserCorrelation.y_data_type == y_data_type
    ).first()

    if not db_correlation:
        return None

    return data_models.CorrelationModel(
        user_id=user_id,
        x_data_type=x_data_type,
        y_data_type=y_data_type,
        correlation=data_models.PearsonCorrelationModel(
            value=db_correlation.value,
            p_value=db_correlation.p_value
        )
    )
