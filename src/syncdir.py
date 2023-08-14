# Agradecimentos: ChatGPT-3.5

import os
import shutil
import configparser

def are_files_equal(file1, file2):
    return os.path.exists(file2) and os.path.getsize(file1) == os.path.getsize(file2) and os.path.getmtime(file1) == os.path.getmtime(file2)

def sync_folders(source, destination):
    for item in os.listdir(source):
        source_item = os.path.join(source, item)
        dest_item = os.path.join(destination, item)

        if os.path.isdir(source_item):
            if os.path.exists(dest_item):
                sync_folders(source_item, dest_item)
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

def main():
    config = configparser.ConfigParser()
    config.read('sync_config.ini')

    for section in config.sections():
        source_folder = config.get(section, 'source')
        dest_folder = config.get(section, 'destination')

        if os.path.exists(source_folder) and os.path.exists(dest_folder):
            print(f"Synchronizing {source_folder} -> {dest_folder}")
            sync_folders(source_folder, dest_folder)
            print("Synchronization complete")
        else:
            print(f"Source or destination folder does not exist for {section}. Skipping...")

if __name__ == "__main__":
    main()
