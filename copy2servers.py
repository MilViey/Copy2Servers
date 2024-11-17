import pandas as pd
import paramiko
import os

def copy_files(ip, remote_path, local_path, username='your_username', password='your_password'):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=username, password=password)
    
    sftp = ssh.open_sftp()
    try:
        sftp.get(remote_path, os.path.join(local_path, os.path.basename(remote_path)))
        print(f"Copied {remote_path} from {ip} to {local_path}")
    except Exception as e:
        print(f"Failed to copy {remote_path} from {ip}: {e}")
    finally:
        sftp.close()
        ssh.close()

def main(excel_file, local_path):
    df = pd.read_excel(excel_file)
    for index, row in df.iterrows():
        copy_files(row['ip'], row['path'], local_path)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Copy files from servers listed in an Excel file.')
    parser.add_argument('excel_file', type=str, help='Path to the Excel file')
    parser.add_argument('local_path', type=str, help='Local path to copy files to')
    args = parser.parse_args()
    
    main(args.excel_file, args.local_path)
