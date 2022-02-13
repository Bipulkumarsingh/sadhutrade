import numpy as np
import pandas as pd
from src.constants import *


def get_reference_days(params):
    if INTERVAL_KEY in params.keys():
        period = params[INTERVAL_KEY]
    else:
        raise ValueError("Please set the corresponding Interval parameter"
                         "{Ct.interval_key(): interval:Ct.INTERVAL.MONTH|Ct.INTERVAL.DAY}")

    if period == INTERVAL.DAY:
        # 252 trading days
        reference_days = 252
    else:
        # 12 months
        reference_days = 12

    return reference_days


def get_cagr(input_df, params=None):
    """"function to calculate the Cumulative Annual Growth Rate of a trading strategy"""

    reference_days = get_reference_days(params)
    df = input_df.copy()
    df.columns = df.columns.droplevel(1)

    cagr_data = (1 + df).cumprod()
    n = len(cagr_data) / reference_days
    result_df = pd.DataFrame()
    result_df["cagr"] = cagr_data.iloc[-1] ** (1 / n) - 1

    return result_df


def get_max_draw_down(input_df):
    """ function to calculate max draw down """

    df = input_df.copy()
    df.columns = df.columns.droplevel(1)

    cumprod_df = (1 + df).cumprod()
    cum_roll_max_df = cumprod_df.cummax()
    drawdown_df = cum_roll_max_df - cumprod_df
    drawdown_pct_df = drawdown_df / cum_roll_max_df
    result_df = pd.DataFrame()
    result_df["MaxDrawDown"] = drawdown_pct_df.max()
    return result_df


def get_calmar(input_df, params=None):
    """function to calculate Calmar"""
    if params is None:
        params = {}

    cagr = get_cagr(input_df, params)
    max_dd = get_max_draw_down(input_df)

    result_df = pd.DataFrame()
    result_df["Calmar"] = (cagr[CAGR_KEY] / max_dd[MAX_DRAWDOWN_KEY])

    return result_df


def get_volatility(input_df, params=None):
    """function to calculate annualized volatility of a trading strategy"""

    if params is None:
        raise ValueError("Please set the corresponding Interval parameter"
                         "{interval:Ct.INTERVAL.MONTH|Ct.INTERVAL.DAY}")

    if NEG_VOLATILITY_KEY not in params.keys():
        params[NEG_VOLATILITY_KEY] = False

    reference_days = get_reference_days(params)
    negative = params[NEG_VOLATILITY_KEY]

    df = input_df.copy()

    df.columns = df.columns.droplevel(1)

    result_df = pd.DataFrame()
    # Whole volatility was calculated
    if negative is False:
        result_df["Volatility"] = (df.std() * np.sqrt(reference_days))

    else:
        df_neg = df.where(df < 0, 0)
        result_df["Volatility"] = (df_neg.std() * np.sqrt(reference_days))

    return result_df


def get_sharpe(input_df, params):
    """ function to calculate sharpe """
    if params is None:
        params = {}

    if "rf" not in params.keys():
        # USA: risk free rate
        params["rf"] = 0.0144

    rf = params["rf"]

    "function to calculate sharpe ratio ; rf is the risk free rate"
    cagr = get_cagr(input_df, params)
    volatility = get_volatility(input_df, params)

    result_df = pd.DataFrame()
    result_df["Sharpe"] = (cagr.loc[:, CAGR_KEY] - rf) / volatility.loc[:, VOLATILITY_KEY]

    return result_df


def get_sortino(input_df, params=None):
    if params is None:
        params = {}

    if "rf" not in params.keys():
        # USA: risk free rate
        params = {"rf": 0.0144}

    rf = params["rf"]

    "function to calculate Sortino ratio ; rf is the risk free rate"

    cagr = get_cagr(input_df, params)

    vol_params = params
    vol_params[NEG_VOLATILITY_KEY] = True
    neg_vol = get_volatility(input_df, vol_params)

    result_df = pd.DataFrame()
    result_df["Sortino"] = (cagr.loc[:, CAGR_KEY] - rf) / neg_vol.loc[:, VOLATILITY_KEY]

    result_df.rename(index={0: "Sortino"}, inplace=True)

    return result_df
