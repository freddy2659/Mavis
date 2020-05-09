from pathlib import Path
import os
import pickle

defaults = {}
defaults['save_dir'] = 'data/'
defaults['sql_file'] = 'sql.cfg'
defaults['pickle_file'] = 'pickle.dat'
defaults['use_sql'] = False  # This is overridden if sql_file exists at startup
defaults['use_pickle'] = True

# If the 'sql_file' exists in 'save_dir', returns True
# Returns 'use_sql'
# Otherwise, False
def use_sql():
    if 'save_dir' in defaults and 'sql_file' in defaults:
        save_path = Path(defaults['save_dir'])
        if save_path.is_dir():
            file_path = Path(f"{defaults['save_dir']}{defaults['sql_file']}")
            if file_path.exists():
                return True
    if 'use_sql' in defaults:
        return defaults['use_sql']
    return False

# Returns 'use_pickle'
# Otherwise, False
def use_pickle():
    if 'use_pickle' in defaults:
        return defaults['use_pickle']
    return False
    
# Returns the data from the pickle file
# Otherwise, None
def load_pickle():
    if use_pickle():
        if 'save_dir' in defaults and 'pickle_file' in defaults:
            # Check the dir
            save_path = Path(defaults['save_dir'])
            if not save_path.is_dir():
                print(f"INFO: Creating save_dir: {defaults['save_dir']}")
                os.makedirs(defaults['save_dir'])
            # Check the file
            file_str = f"{defaults['save_dir']}{defaults['pickle_file']}"
            file_path = Path(file_str)
            if not file_path.exists():
                print(f"INFO: Pickle file doesn't exist yet: {file_str}")
                return None
            with open(file_str, 'rb') as f:
                print(f"INFO: Loading pickle data from: {file_str}")
                try:
                    save_data = pickle.load(f)
                except EOFError as e:
                    print("Failed to load_pickle(): End of File Error. Is the file empty?")
                    return None
                return save_data
        print("Failed to load_pickle(). Check save_dir and pickle_file are set in the defaults.py")
    return None
    
def save_pickle(data):
    if use_pickle():
        if 'save_dir' in defaults and 'pickle_file' in defaults:
            # Check the dir
            save_path = Path(defaults['save_dir'])
            if not save_path.is_dir():
                print(f"INFO: Creating save_dir: {defaults['save_dir']}")
                try:
                    os.makedirs(defaults['save_dir'])
                except OSError as e:
                    if e.errno != e.EXIST or not os.path.isdir(defaults['save_dir']):
                        print(f"Cannot create the save_dir: {defaults['save_dir']}")
                        raise
            file_str = f"{defaults['save_dir']}{defaults['pickle_file']}"
            with open(file_str, 'wb') as f:
                pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
            return
        print("Failed to save_pickle(). Check save_dir and pickle_file are set in the defaults.py")
    return

def load_sql(existing):
    #TODO: This is a stub
    raise NotImplementedError("load_sql hasn't been implemented")
    if use_sql():
        if existing is None:
            # Purely load the SQL
            print("TODO: Load SQL")
        else:
            # Merge the SQL
            print("TODO: Merge SQL")
    return existing
    