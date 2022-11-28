from datetime import datetime
from dateutil.relativedelta import relativedelta

six_months_before_date = datetime.today() - relativedelta(months=+6)
six_months_after_date = datetime.today() + relativedelta(months=+6)

str_obj = '2022-11-26'
date_obj = datetime.strptime(str_obj, '%Y-%m-%d')
date_obj_new = datetime.strptime(date_obj, '%Y-%m-%d')
# if date_obj > six_months_before_date:
#     print("True")
print(type(date_obj_new))