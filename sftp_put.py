import paramiko
import os

host = os.getenv('REMOTE_HOST')
password = os.getenv("REMOTE_PAS")

transport = paramiko.Transport((host, 22))
transport.connect(username='root', password=password)
# transport.connect()

sftp = paramiko.SFTPClient.from_transport(transport)#如果连接需要密钥，则要加上一个参数，hostkey="密钥"
 
sftp.put('release/release.zip', '/home/docker/nginx/download/release.zip')
sftp.put('release/update/release.zip', '/home/docker/nginx/download/update/release.zip')
 
transport.close()#关闭连接