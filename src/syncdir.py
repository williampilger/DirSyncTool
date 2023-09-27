import os
import shutil
import configparser
import fnmatch
import subprocess
from datetime import datetime

LOG_FILE = "log_geral.txt"

def somar_dicionarios(dict1, dict2):
    resultado = {}
    for chave in dict1:
        if isinstance(dict1[chave], int):
            resultado[chave] = dict1[chave] + dict2[chave]
        elif isinstance(dict1[chave], dict):
            resultado[chave] = somar_dicionarios(dict1[chave], dict2[chave])
    return resultado

class FilesHandler:
    
    counter_control = {'ignored':0, 'cp': 0, 'compress':0, 'rm': 0, 'cptree':0,'rmtree': 0,'errors':{'cp': 0, 'rm': 0, 'cptree':0, 'rmtree': 0, 'other': 0} }

    def __init__(self, ignore_patterns = []):
        self.ignore_patterns = ignore_patterns

    def update_ignore_patterns(self, ignore_patterns):
        self.ignore_patterns = ignore_patterns
    
    def should_ignore_file(self, file_name):
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(file_name, pattern):
                self.counter_control['ignored'] += 1
                return True
        return False
    
    def are_files_equal(self, file1, file2):
        return os.path.exists(file2) and os.path.getsize(file1) == os.path.getsize(file2) and int(os.path.getmtime(file1)) == int(os.path.getmtime(file2))

    def copytree(self, source, destination):
        try:
            shutil.copytree(source, destination)
            print(f"    copytree: {source} -> {destination}")
            self.counter_control['cptree'] += 1
            return True
        except Exception as e:
            self.counter_control['errors']['cptree'] += 1
            registra_log_geral(f"    copytree: {source} -> {destination} = Error: {e}")
        return False
    
    def copy2(self, source, destination):
        try:
            shutil.copy2(source, destination)
            print(f"    copy2: {source} -> {destination}")
            self.counter_control['cp'] += 1
            return True
        except Exception as e:
            self.counter_control['errors']['cp'] += 1
            registra_log_geral(f"    copy2: {source} -> {destination} = Error: {e}")
        return False
    
    def rmtree(self, path):
        try:
            shutil.rmtree(path)
            print(f"    rmtree: {path}")
            self.counter_control['rmtree'] += 1
            return True
        except Exception as e:
            self.counter_control['errors']['rmtree'] += 1
            registra_log_geral(f"    rmtree: {path} = Error: {e}")
        return False

    def remove(self, path):
        try:
            os.remove(path)
            print(f"    remove: {path}")
            self.counter_control['rm'] += 1
            return True
        except Exception as e:
            self.counter_control['errors']['rm'] += 1
            registra_log_geral(f"    remove: {path} = Error: {e}")
        return False
    
    def sync_folders(self, source, destination ):
        try:
            for item in os.listdir(source):
                
                if self.should_ignore_file(item):
                    continue

                source_item = os.path.join(source, item)
                dest_item = os.path.join(destination, item)

                if os.path.isdir(source_item):
                    if os.path.exists(dest_item):
                        self.sync_folders( source_item, dest_item)
                    else:
                        self.copytree(source_item, dest_item)
                else:
                    if not self.are_files_equal(source_item, dest_item):
                        self.copy2(source_item, dest_item)

            for item in os.listdir(destination):
                source_item = os.path.join(source, item)
                dest_item = os.path.join(destination, item)

                if not os.path.exists(source_item):
                    if os.path.isdir(dest_item):
                        self.rmtree(dest_item)
                    else:
                        self.remove(dest_item)
            return True
        except Exception as e:
            self.counter_control['errors']['other'] += 1
            print(f"  Sync({source}->{destination}) = Error: {e}")
            registra_log_geral(f"  Erro: {e}")
        return False
    
    def compact_folder( self, source, destination, size='' ):
        try:
            ignore = ''
            for ign in self.ignore_patterns:
                if ignore != '':
                    ignore += ' '
                ignore += '-xr!' + ign
            
            if( size != ''):
                size = '-v' + size

            print(f'7z a {ignore} {size} "{destination}" "{source}"')
            os.system( f'7z a {ignore} {size} "{destination}" "{source}"' )
            self.counter_control['compress'] += 1
            return True
        except Exception as e:
            self.counter_control['errors']['other'] += 1
            print(f"  Compact({source}->{destination}) = Error: {e}")
            registra_log_geral(f"  Erro: {e}")
        return False

    def get_counter_control(self):
        return self.counter_control

    def print_counter_control(self):
        print(f"    {self.counter_control}")
        try:
            with open(LOG_FILE, "a") as arquivo:
                arquivo.writelines(f'\n*********************************************************************\n RELATORIO DE SINCRONIZACAO')
                arquivo.writelines(f"\n Arquivos Copiados:  {self.counter_control['cp']}")
                arquivo.writelines(f"\n Compressões:        {self.counter_control['compress']}")
                arquivo.writelines(f"\n Pastas Copiados:    {self.counter_control['cptree']}")
                arquivo.writelines(f"\n Arquivos Removidos: {self.counter_control['rm']}")
                arquivo.writelines(f"\n Pastas Removidas:   {self.counter_control['rmtree']}")
                arquivo.writelines(f"\n Ignorados:          {self.counter_control['ignored']}")
                arquivo.writelines(f"\n ERROS:")
                arquivo.writelines(f"\n   Cópia de Arquivo:   {self.counter_control['errors']['cp']}")
                arquivo.writelines(f"\n   Cópia de Pasta:     {self.counter_control['errors']['cptree']}")
                arquivo.writelines(f"\n   Remoção de Arquivo: {self.counter_control['errors']['rm']}")
                arquivo.writelines(f"\n   Remoção de Pasta:   {self.counter_control['errors']['rmtree']}")
                arquivo.writelines(f"\n   Outros erros:       {self.counter_control['errors']['other']}")
                arquivo.writelines(f'\n*********************************************************************')
        except:
            pass
        return


def registra_log_geral(texto):
    instante = datetime.now().strftime('%d/%m/%Y\t%H:%M:%S')
    print(f"{instante}\t{texto}")
    try:
        with open(LOG_FILE, "a") as arquivo:
            arquivo.writelines(f"\n{instante}\t{texto}")
    except:
        pass
    return

def main():
    config = configparser.ConfigParser()
    fh = fh = FilesHandler()
    config.read('sync_config.ini')
    for section in config.sections():
        source_folder = config.get(section, 'source')
        dest_folder = config.get(section, 'destination')
        mode = config.get(section, 'mode', fallback='normal')
        fh.update_ignore_patterns( [ pattern.strip() for pattern in config.get(section, 'ignore_patterns', fallback='').split(',')] )

        if mode == 'normal':
            if os.path.exists(source_folder) and os.path.exists(dest_folder):
                registra_log_geral(f"  Synchronizing {source_folder} -> {dest_folder}")
                if fh.sync_folders(source_folder, dest_folder):
                    registra_log_geral("  Synchronization complete")
                else:
                    registra_log_geral("  Synchronization failed")
            else:
                registra_log_geral(f"  Source or destination folder does not exist for {section}. Skipping...")
        elif mode.startswith('compress'):
            md = mode.split('_')
            size = ''
            if len(md) > 1:
                size = md[1]
            registra_log_geral(f"  Compressing {source_folder} -> {dest_folder}")
            if fh.compact_folder(source_folder, dest_folder, size):
                registra_log_geral("  Compression complete")
            else:
                registra_log_geral("  Compression failed")
        else:
            registra_log_geral("  Invalid mode informed")
    fh.print_counter_control()

if __name__ == "__main__":
    registra_log_geral("Starting main synchronization (Version 2.0)")
    main()
    registra_log_geral("Main synchronization complete\n\n")
