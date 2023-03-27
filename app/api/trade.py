import datetime

import dateutil.parser
from flask import request, json
from . import bp
from .auth import token_required

import os
import numpy as np
import pandas as pd


@bp.route('/instrument_futs_latest', methods=['POST'])
@token_required
def get_futs_table():

    from falcon.loader.fut import QuantDB

    # define the list of futures to retrieve
    nmes = ('CBOT_W', 'ICE_SB', 'NYMEX_CO', 'NYMEX_CL', 'CBOT_KW', 'CME_LC',
            'NYMEX_NG', 'CBOT_S', 'ICE_KC', 'CBOT_C')

    # get data from the DB
    cred = os.environ['DATABASE_URL']
    df = QuantDB.DashSupport.get_latest_brief(nmes, cred, 'url', n_tenor=3)
    # df.delivery_month = df.delivery_month.dt.strftime('%b-%y')

    res = df.to_json(orient='records', date_format='iso')

    return json.loads(res)


@bp.route('/instrument_futs_plot', methods=['POST'])
@token_required
def get_futs_plot():

    from falcon.loader.fut import QuantDB
    from datetime import date, datetime, timedelta
    from pandas.tseries.offsets import BDay

    cred = os.environ['DATABASE_URL']

    # define the futures contract to retrieve
    fut_code = request.json.get('futures_code', 'CBOT_W')
    delivery_month = dateutil.parser.isoparse(request.json.get('delivery_month', '2022-12-01'))
    delivery_month = delivery_month.replace(day=1).date()

    # fut_code = 'CBOT_W'
    # delivery_month = pd.Timestamp('2022-12-01')

    # define the start and end dates
    end_date = (datetime.today() - BDay(1)).date()
    start_date = end_date - timedelta(days=365*2)

    # get data from the DB
    df_fut = QuantDB.load_specific_fut(
        fut_code, delivery_month, start_date, end_date, cred, 'url')

    # interpolate NaN values
    df_fut.set_index(['settle_date'], inplace=True)
    df_fut = df_fut.apply(pd.to_numeric, downcast='float')
    df_fut.interpolate(axis=0, inplace=True)

    df_fut.reset_index(inplace=True)

    res = df_fut.to_json(orient='records', date_format='iso')

    return json.loads(res)


@bp.route('/instrument_futs_plot/fcst', methods=['POST'])
@token_required
def get_futs_plot_fcst():

    import falcon.simulator.scenario_generator as sg

    from falcon.loader.fut import QuantDB
    from falcon.utils import mis

    cred = os.environ['DATABASE_URL']

    # define the futures contract to retrieve
    fut_code = request.json.get('futures_code', 'CBOT_W')  # DONE: to be replaced by the input fut_code
    tenor = 1
    start_date = pd.Timestamp(2000, 1, 1)
    end_date = pd.to_datetime('today').normalize() - pd.to_timedelta(1, 'D')

    # get futures data
    df_fut = QuantDB.load_generic_fut(
        fut_code, tenor, start_date, end_date, cred, 'url')
    df_fut = df_fut[['settle_date', 'px_last']]
    df_fut.set_index(['settle_date'], inplace=True)
    end_date = df_fut.last_valid_index()
    df_fut = df_fut.apply(pd.to_numeric, downcast='float')  # TODO: original data are Decimal objects

    df_fut.interpolate(inplace=True)

    # configure the scenario generator
    sg_mapping = {
        "Backtest": "Backtesting",
        "HS": "HistSimulation",
        "fHS": "FilteredHistSim",
        "fHSB": "FilteredHistSimBootstrap",
        "GBM": "GBM"
    }
    sg_eng = getattr(sg, sg_mapping[request.json.get('sg_eng', 'fHS')])  # DONE: to be replaced
    len_path = int(request.json.get('len_path', 150))  # DONE: to be replaced, in number of days
    len_seed = 100  # TODO: to be pre-defined

    # estimate EWMA vol
    ts_ret = (np.log(df_fut) - np.log(df_fut.shift(1))).iloc[1:, 0]
    ewma_lbd = 0.97  # TODO: to be pre-defined
    ts_vol = mis.calc_ewma_vol(ts_ret, ewma_lbd)

    ls_scenarios, scenario_prices = sg_eng.gen_scenarios_path(
        df_fut, ts_vol, end_date, len_path, len_seed)

    base_price = float(request.json.get('base_price', 100))  # DONE: to be replaced by the current price of the specific futures contract

    scenario_prices_adapted = sg_eng.adapt_scenarios_path(
        base_price, scenario_prices)

    fcst_mean = np.mean(scenario_prices_adapted, axis=0)
    fcst_lb, fcst_ub = np.quantile(scenario_prices_adapted, [0.05, 0.95],
                                   axis=0)
    ls_dates = pd.bdate_range(end_date, periods=len_path, freq='B')

    df = pd.DataFrame({
        'date': ls_dates,
        'mean': fcst_mean,
        'lower_bound': fcst_lb,
        'upper_bound': fcst_ub,
    })

    res = df.to_json(orient='records', date_format='iso')

    return json.loads(res)


@bp.route('/instrument_futs_margin', methods=['POST'])
@token_required
def get_futs_margin():
    fut_code = request.json.get('futures_code', 'CBOT_W')
    delivery_month = dateutil.parser.isoparse(request.json.get('delivery_month', '2022-12-01'))
    delivery_month = delivery_month.replace(day=1).date()

    from falcon.loader.fut import QuantDB

    cred = os.environ['DATABASE_URL']
    res = QuantDB.load_latest_margin(fut_code, delivery_month, cred, 'url')

    return {'value': res}


@bp.route('/instrument_futs_curve', methods=['POST'])
@token_required
def get_futs_curve():

    fut_code = request.json.get('futures_code', 'CBOT_W')
    date = pd.to_datetime('today').normalize() - pd.to_timedelta(1, 'D')

    from falcon.loader.fut import QuantDB

    cred = os.environ['DATABASE_URL']
    df = QuantDB.load_fut_curve(fut_code, date, cred, 'url')

    res = df.to_json(orient='records', date_format='iso')

    return json.loads(res)


@bp.route('/instrument_futs_orderbook', methods=['POST'])
@token_required
def get_futs_orderbook():  # dummy data

    from falcon.loader.fut import QuantDB
    res = QuantDB.DashSupport.get_order_book()

    return res
