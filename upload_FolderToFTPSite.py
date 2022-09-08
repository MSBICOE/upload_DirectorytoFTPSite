"""
Created by Steven Wang for website or nested directory uploading to an FTP site.
"""
from ftpretty import ftpretty
from pathlib import Path
import os
import timeit
from contextlib import contextmanager

## set context for time elapse display
@contextmanager
def timeused(msg):
    start = timeit.default_timer()
    try:
        yield
    finally:
        end = timeit.default_timer()
        time_elapse = round((end - start) / 60, 2)
        print (f'{msg} The total upload time elapsed is: {time_elapse} minutes')

def upload_EntireDirectoryToFTPSite(Local_Directory, FTP_Site_Directory, FTP_Site, username, password, passive = True):  
    """
    Funcion name: upload_EntireDirectoryToFTPSite
    usage: this function is used to upload a full local directory to a remote ftp site. 

    Args:
        Local_Directory (str): the local file directory, like "c:/apps/mywebsite"
        FTP_Site_Directory (str): the directory in ftp site, if it is root then "/", otherwise like "/myblog"
        FTP_Site (str): ftp site hostname
        username (str): your ftp user name
        password (str): your ftp password
        passive (bool, optional): change the FTP mode to either passvie or active. Defaults to True, which is passive.
    """
    
    ## change the working directory to the local directory which you want to upload to ftp site
    path = Path(Local_Directory)
    os.chdir(path)
    
    with timeused(f'File Directory "{Local_Directory}" has fully uploaded to "{FTP_Site}" under directory {FTP_Site_Directory}.'):
    # f = ftpretty("ftp.smartspreadsheet.com", "0102281|smartspread", "iasfatr061")
        f = ftpretty(FTP_Site, username, password)
        f.cd(FTP_Site_Directory)  
        remote_list = f.list()

        for p in sorted(path.rglob('*')):
            if p.is_dir():
                p_remote = p.relative_to(path)
                # print(p_remote.parts)
                if len(p_remote.parts) == 1:
                    p_remote_list = remote_list
                else:
                    parents = p_remote.parts[0:-1]
                    print(parents)
                    p_parents = path.joinpath(*parents).relative_to(path)
                    print(p_parents)
                    p_remote_list = [str(p_parents / l) for l in  f.list(str(p_parents))]
                
                # print(p_remote)  
                # print(p_remote_list) 
                            
                if str(p_remote) not in p_remote_list:
                    f.mkdir(str(p_remote))
                    print(f"{p_remote} created in the remote ftp server.")
                else:
                    print(f"{p_remote} is already in ftp site")
                    
        for fl in sorted(path.rglob('*')):
            if fl.is_file():
                f_remote = fl.relative_to(path)
                # print(f_remote.parent)
                if len(f_remote.parts) == 1:
                    f.cd(FTP_Site_Directory)
                    # print("yue")
                else:
                    f_parent = Path(FTP_Site_Directory) / f_remote.parent
                    f.cd(str(f_parent))
                f.put(fl.relative_to(path), str(fl.relative_to(path).name))
                print(str(fl.relative_to(path)))
                
        f.close()            

if __name__ == "__main__":
    
    ## assign the parameter values
    params = {"Local_Directory": "Your_Local_Directory", 
              "FTP_Site_Directory": "FTP_Site_Directory", 
              "FTP_Site": "FTP_HostName", 
              "username": "Your FTP Username", 
              "password": "Your FTP Password"
            }
    
    upload_EntireDirectoryToFTPSite(**params)
