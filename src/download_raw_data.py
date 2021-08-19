"""""
This script downloads the data needed for analysis from the Minsa database.
 It uses series that are in the yaml config file.
"""

from datetime import date
import urllib
from urllib import request
import os
import progressbar
import src.utilities as utils



def create_path():
    
    config = utils.read_config()
    # Get date for the filename.
    today = date.today()
    date_str = today.strftime("%b_%d_%Y")
    
    # Define the filename and path to download it.
    path =  os.path.join(config['data']['rawFilePath'], f'fallecidos_sinadef_{date_str}.csv')
    return path

def check_path_existance(path):
    
    """
    Iterate over files in that directory 
    to see if it already exists.
    """
    config = utils.read_config()
    for item in os.scandir(config['data']['rawFilePath']):
        if item.is_file():
            if item.name in path:
                print("\nFile already up-to-date.")
                print(f"File found: {item.name}\n")
                break
            
    else:
        download_raw_data(path)
        
def download_raw_data(path):
    
    print("\nDownloading file...\n'")
    # Define url to download the file from.
    url = 'https://cloud.minsa.gob.pe/s/nqF2irNbFomCLaa/download'
       
    # Open url to avoid Error 403 (forbidden)
    opener = urllib.request.URLopener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36  (KHTML, like Gecko) Chrome/36.0.1941.0  Safari/537.36')]
    
    # Download file.
    opener.retrieve(url, path, show_progress)
    print('Download finished.\n')
    
pbar = None

def show_progress(block_num, block_size, total_size):
    """ ProgressBar setting. (for UX)"""
    
    global pbar 
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None    


def main():
    path = create_path()
    check_path_existance(path)
    
if __name__ == "__main__":
    main()    
    
    













