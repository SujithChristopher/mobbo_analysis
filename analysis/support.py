import numpy as np
from scipy.signal import interp1d

def slice_data(df):
    
    # trunkate dfs
    _temp_df = df
    _start_inx = None
    _end_inx = None
    _trailing_trigger = False
    for i in range(len(_temp_df['sync'])):
        if (_temp_df['sync'][i] == 1) and (not _trailing_trigger):
            _start_inx = i
            _trailing_trigger = True
        
        if (_temp_df['sync'][i] == 0) and (_trailing_trigger):
            _end_inx = i
            break
    _temp_df = _temp_df[_start_inx:_end_inx]   
    return _temp_df

def interpolate(df, ref_df):
    # df is the df to be interpolated
    # ref_df is the reference df
    # df and ref_df should have the same columns
    
    columns = df.columns[1:-1]
    
    interp_func = []
    for _col in columns:
        interp_func.append(interp1d(ref_df['time'], ref_df[columns], kind='linear', axis=0, fill_value='extrapolate'))
    
    for i in range(len(df['time'])):
        for j in range(len(columns)):
            df[columns[j]][i] = interp_func[j](df['time'][i])
    
    return df

def interpolats_dfs(dfs, ref_no = 0):
    # generally first df is the reference df
    
    _reference_df = dfs[ref_no]
    columns = _reference_df.columns[1:-1]
    
    interp_func = []
    for _col in columns:
        interp_func.append(interp1d(_reference_df['time'], _reference_df[columns], kind='linear', axis=0, fill_value='extrapolate'))
    
    
    return dfs
    
    
    

def preprocess(dfs):
    for _name in dfs.keys():
        dfs[_name] = slice_data(dfs[_name])
        
    return dfs