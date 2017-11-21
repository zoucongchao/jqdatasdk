# coding=utf-8
from functools import wraps
from .utils import *


data_client = None


def assert_auth(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        if data_client is None:
            print("run jqdatasdk.init fist")
        else:
            return func(*args, **kwargs)
    return _wrapper


@assert_auth
def get_price(security, start_date=None, end_date=None, frequency='daily', 
    fields=None, skip_paused=False, fq='pre', count=None):
    security = convert_security(security)
    start_date = to_date_str(start_date)
    end_date = to_date_str(end_date)
    if (not count) and (not start_date):
            start_date = "2015-01-01"
    if count and start_date:
        raise ParamsError("(start_date, count) only one param is required")
    return data_client.get_price(**locals())


@assert_auth
def get_trade_days(start_date=None, end_date=None, count=None):
    start_date = to_date_str(start_date)
    end_date = to_date_str(end_date)
    data = data_client.get_trade_days(**locals())
    return [to_date(i.item()) for i in data]


@assert_auth
def get_all_trade_days():
    data = data_client.get_all_trade_days()
    return [to_date(i.item()) for i in data]


@assert_auth
def get_extras(info, security_list, start_date=None, end_date=None, df=True, count=None):
    start_date = to_date_str(start_date)
    end_date = to_date_str(end_date)
    security_list = convert_security(security_list)
    return data_client.get_extras(**locals())


@assert_auth
def get_index_stocks(index_symbol, date=today()):
    assert index_symbol, "index_symbol is required"
    date = to_date_str(date)
    return data_client.get_index_stocks(**locals())


@assert_auth
def get_industry_stocks(industry_code, date=today()):
    assert industry_code, "industry_code is required"
    date = to_date_str(date)
    return data_client.get_industry_stocks(**locals())


@assert_auth
def get_concept_stocks(concept_code, date=today()):
    assert concept_code, "concept_code is required"
    date = to_date_str(date)
    return data_client.get_concept_stocks(**locals())


@assert_auth
def get_all_securities(types=[], date=None):
    date = to_date_str(date)
    return data_client.get_all_securities(**locals())


@assert_auth
def get_security_info(code):
    assert code, "code is required"
    result = data_client.get_security_info(**locals())
    if result:
        return Security(**result)


@assert_auth
def get_money_flow(security_list, start_date=None, end_date=None, fields=None, count=None):
    assert security_list, "security_list is required"
    security_list = convert_security(security_list)
    start_date = to_date_str(start_date)
    end_date = to_date_str(end_date)
    return data_client.get_money_flow(**locals())


@assert_auth
def get_fundamentals(query_object, date=None, statDate=None):
    from .finance_service import get_fundamentals_sql
    if date is None and statDate is None:
        date = datetime.date.today()
        from .calendar_service import CalendarService
        trade_days = CalendarService.get_all_trade_days()
        date = list(filter(lambda item: item < date, trade_days))[-1]
    elif date:
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        date = min(to_date(date), yesterday)
    sql = get_fundamentals_sql(query_object, date, statDate)
    return data_client.get_fundamentals(sql=sql)


@assert_auth
def get_mtss(security_list, start_date=None, end_date=None, fields=None, count=None):
    assert (not start_date) ^ (not count), "(start_date, count) only one param is required"
    start_date = to_date_str(start_date)
    end_date = to_date_str(end_date)
    security_list = convert_security(security_list)
    return data_client.get_mtss(**locals())


@assert_auth
def get_future_contracts(underlying_symbol, dt=None):
    assert underlying_symbol, "underlying_symbol is required"
    dt = to_date_str(dt)
    return data_client.get_future_contracts(**locals())


@assert_auth
def get_dominant_future(underlying_symbol, dt=None):
    dt = to_date_str(dt)
    return data_client.get_dominant_future(**locals())


@assert_auth
def normalize_code(code):
    return data_client.normalize_code(**locals())


def read_file(path):
    with open(path, 'rb') as f:
        return f.read()


def write_file(path, content, append=False):
    if isinstance(content, six.text_type):
        content = content.encode('utf-8')
    with open(path, 'ab' if append else 'wb') as f:
        return f.write(content)


__all__ = ["get_price", "get_trade_days", "get_all_trade_days", "get_extras", 
            "get_index_stocks", "get_industry_stocks", "get_concept_stocks", "get_all_securities",
            "get_security_info", "get_money_flow", "get_fundamentals", "get_mtss", "get_future_contracts", 
            "get_dominant_future", "normalize_code", "read_file", "write_file"]

