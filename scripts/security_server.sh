cd C:/Users/$USERNAME/Desktop/proyectos/swarm-automations
export PYTHONPATH=/c/Users/$USERNAME/Desktop/proyectos/swarm-automations:/c/Users/$USERNAME/Desktop/proyectos/eigenlib
source .venv/Scripts/activate
export PYTHONUNBUFFERED=1
python -c "
import time
from swarmautomations.main import NanoNetMainClass
################################################################################################################
def encryption_aux(public_key):
	from cryptography.fernet import Fernet
	from dotenv import dotenv_values
	encryption = Fernet(public_key)
	env_vars = dotenv_values(r'C:\Users\apren\Desktop\.env')
	encrypted_vars = {k: encryption.encrypt(v.encode()).decode() for k, v in env_vars.items()}
	return encrypted_vars
config = {
	'node_method': encryption_aux,
	'master_address': 'tcp://95.18.166.44:5005',
	'node_name': 'security_node',
	'password': 'youshallnotpass',
	'delay': 5,
		}
################################################################################################################
main = NanoNetMainClass(config)
print('Security server started.')
main.launch_personal_server_node(config)
while True:
	time.sleep(1)
"