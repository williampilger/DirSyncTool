# Agradecimentos ao ChatGPT-3.5, que escreveu a maior parte do código.

import os
import shutil
import configparser
import fnmatch
from datetime import datetime

def should_ignore_file(file_name, ignore_patterns):
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(file_name, pattern):
            return True
    return False

def are_files_equal(file1, file2):
    return os.path.exists(file2) and os.path.getsize(file1) == os.path.getsize(file2) and int(os.path.getmtime(file1)) == int(os.path.getmtime(file2))

def sync_folders(source, destination, ignore_patterns):
    try:
        for item in os.listdir(source):
            
            if should_ignore_file(item, ignore_patterns):
                continue

            source_item = os.path.join(source, item)
            dest_item = os.path.join(destination, item)

            if os.path.isdir(source_item):
                if os.path.exists(dest_item):
                    sync_folders(source_item, dest_item, ignore_patterns)
                else:
                    print(f"copytree: {source_item}")
                    shutil.copytree(source_item, dest_item)
            else:
                if not are_files_equal(source_item, dest_item):
                    print(f"copy2: {source_item}")
                    shutil.copy2(source_item, dest_item)

        for item in os.listdir(destination):
            source_item = os.path.join(source, item)
            dest_item = os.path.join(destination, item)

            if not os.path.exists(source_item):
                if os.path.isdir(dest_item):
                    print(f"rmtree: {dest_item}")
                    shutil.rmtree(dest_item)
                else:
                    print(f"remove: {dest_item}")
                    os.remove(dest_item)
        return True
    except Exception as e:
        print(f"Sync({source}->{destination}) = Error: {e}")
        registra_log_geral(f"Erro: {e}")
    return False

def registra_log_geral(texto):
    instante = datetime.now().strftime('%d/%m/%Y\t%H:%M:%S')
    print(f"{instante}\t{texto}")
    try:
        with open("log_geral.txt", "a") as arquivo:
            arquivo.writelines(f"\n{instante}\t{texto}")
    except:
        pass
    return

def main():
    config = configparser.ConfigParser()
    config.read('sync_config.ini')

    for section in config.sections():

        source_folder = config.get(section, 'source')
        dest_folder = config.get(section, 'destination')
        ignore_patterns = config.get(section, 'ignore_patterns', fallback='').split(',')

        if os.path.exists(source_folder) and os.path.exists(dest_folder):
            registra_log_geral(f"Synchronizing {source_folder} -> {dest_folder}")
            if sync_folders(source_folder, dest_folder, ignore_patterns):
                registra_log_geral("Synchronization complete")
            else:
                registra_log_geral("Synchronization failed")
        else:
            registra_log_geral(f"Source or destination folder does not exist for {section}. Skipping...")

if __name__ == "__main__":
    main()
