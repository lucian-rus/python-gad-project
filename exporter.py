import pandas as pd

from utils import format_string, debug_data

def exporter_to_csv(data, name):
    data_list = []

    for obj in data: 
        row_list = []      
        row_list.append(obj.country_name)
        row_list.append(int(format_string(obj.total_cases)))
        row_list.append(int(format_string(obj.total_deaths)))
        row_list.append(int(format_string(obj.new_cases)))
        row_list.append(int(format_string(obj.new_deaths)))
        row_list.append(int(format_string(obj.population)))

        data_list.append(row_list)

    data_frame = pd.DataFrame(data_list)
    data_frame.to_csv('output/' + name)
    debug_data('done. exported to `output/' + name +'`')
