"""
This script pre-process the data
"""
from datetime import date
import os
import src.utilities as utils
import numpy as np
import pandas as pd

def create_path():
    
    config = utils.read_config()
    # Get date for the filename.
    today = date.today()
    date_str = today.strftime("%b_%d_%Y")
    
    # Define the filename and path to download it.
    path =  os.path.join(config['data']['rawFilePath'], f'fallecidos_sinadef_{date_str}.csv')
    return path



def preprocess_data():
    
    """
    input: dataset
    output: clean dataset
    """
    path = create_path()
    df = pd.read_csv(path, delimiter= '|')
    df.rename(columns= {df.columns[0]: 'ID'}, inplace = True)
    
    """cols_to_keep = ['ID', 'TIPO SEGURO', 'SEXO', 'EDAD', 'TIEMPO EDAD',
       'PAIS DOMICILIO', 'DEPARTAMENTO DOMICILIO',
       'PROVINCIA DOMICILIO', 'DISTRITO DOMICILIO', 'FECHA', 'TIPO LUGAR',
       'DEBIDO A (CAUSA A)', 'DEBIDO A (CAUSA B)', 'DEBIDO A (CAUSA C)',
       'DEBIDO A (CAUSA D)', 'DEBIDO A (CAUSA E)', 'DEBIDO A (CAUSA F)']"""   
          
    #cols_to_drop = [x for x in df.columns if x != cols_to_keep]
    cols_to_drop= ['MUERTE VIOLENTA', 'NECROPSIA', 'CAUSA A (CIE-X)','CAUSA B (CIE-X)', 'CAUSA C (CIE-X)', 'CAUSA D (CIE-X)', 'CAUSA E (CIE-X)', 'CAUSA F (CIE-X)', 'INSTITUCION', 'NIVEL DE INSTRUCCIÓN', 'AÑO', 'MES', 'ESTADO CIVIL' ]
    df.drop(cols_to_drop, axis=1, errors = 'ignore', inplace=True)
    
    # Column labels preprocessing.
    df.columns = df.columns.str.lower()
    df.columns = [col.replace(" ", "_") for col in df.columns]
    
    # Replacing SIN REGISTRO and IGNORADO entries for NAs
    df.replace(['SIN REGISTRO','IGNORADO'], np.nan, inplace=True)
    
    # Dtype to numeric
    df['edad'] = df['edad'].apply(pd.to_numeric)
   
    # Dtype to timestamp
    df['fecha'] = df['fecha'].apply(lambda x: pd.Timestamp(x))
    
    # Cast everything to lowercase except for non strings.
    df = df.applymap(lambda s:s.lower() if type(s) == str else s)
    
    # normalize records strings
    cols = df.select_dtypes(include=[np.object]).columns
    df[cols] = df[cols].apply(lambda x: x.str.normalize('NFKD')
                                         .str.encode('ascii', errors='ignore')
                                         .str.decode('utf-8'))
    
    # normalize column names strings
    df.columns = (df.columns.str.normalize('NFKD')
                            .str.encode('ascii', errors='ignore')
                            .str.decode('utf-8'))
    
    return df
    
def create_clean_data():
    
    # Get config file
    config = utils.read_config()
    
    df = preprocess_data()
    # Write clean data
    df.to_csv(os.path.join(config['data']['clnFilePath'], 'ts_data.csv'))
    
if __name__ == "__main__":
    # Master function
    create_clean_data()    