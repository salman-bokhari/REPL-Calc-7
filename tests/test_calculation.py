from app.calculation import Calculation
from datetime import datetime
def test_calc_to_dict():
    c = Calculation('add',1,2,3, datetime.now())
    d = c.to_dict()
    assert d['operation']=='add'
    assert float(d['result'])==3.0
