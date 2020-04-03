import subprocess
ssh=subprocess.Popen(r'explorer /select,"C:\Users\NovaGamma\Desktop\game_project\level editor"',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
result = ssh.stdout.readlines()
print (result)