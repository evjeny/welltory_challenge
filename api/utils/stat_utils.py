from datetime import date

import numpy as np
from scipy.stats import pearsonr

from models.data_models import DateStatModel, PearsonCorrelationModel


def calculate_pearson_correlation(x: list[DateStatModel], y: list[DateStatModel]) -> PearsonCorrelationModel | None:
    x_mapping: dict[date, float] = {date_stat.date: date_stat.value for date_stat in x}
    simultaneous_data = [
        (x_mapping[date_stat.date], date_stat.value)
        for date_stat in y
        if date_stat.date in x_mapping
    ]

    if len(simultaneous_data) < 2:
        return None
    
    data = np.array(simultaneous_data)
    coef, p_value = pearsonr(data[:, 0], data[:, 1])
    
    return PearsonCorrelationModel(value=coef, p_value=p_value)
