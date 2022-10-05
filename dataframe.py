import json

import pandas as pd


def create_dictionary(company_categories, dataframe):
    master_dict = dict()
    for cateogry in company_category:
        edited_df = df.loc[df[cateogry] == 1]
        master_dict[cateogry] = list(edited_df['Company_Name'])
    return master_dict


df = pd.read_excel('similarcompanies1.xlsx', header=2)
cols = df.columns
cols = list(cols)
cols.pop(0)
cols.pop(0)
cols.pop(0)

company_category = cols
returned_dict = create_dictionary(company_categories = company_category, dataframe= df)

json_data = json.dumps(returned_dict, indent=5)
json_file = open('Category_wise_data.json', 'w')
json_file.write(json_data)



