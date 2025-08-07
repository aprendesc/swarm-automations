cd C:/Users/$USERNAME/Desktop/proyectos/swarm-automations
export PYTHONPATH=/c/Users/$USERNAME/Desktop/proyectos/swarm-automations:/c/Users/$USERNAME/Desktop/proyectos/eigenlib
source .venv/Scripts/activate
export PYTHONUNBUFFERED=1
python -c "
from swarmautomations.main import MainClass
from cryptography.fernet import Fernet
################################################################################################################
public_key = Fernet.generate_key()
config = {
	'master_address': 'tcp://95.18.166.44:5005',
	'payload': {'public_key': public_key},
	'password': 'youshallnotpass',
	'address_node': 'security_node',
	'delay': 5,
}
################################################################################################################
main = MainClass(config)
output_config = main.call_personal_server_node(config)
encrypted_vars = output_config['response']
f = Fernet(public_key)
env_vars = {k: f.decrypt(v.encode()).decode() for k, v in encrypted_vars.items()}
print(env_vars)
if False:
	def save_env_dict(env_vars, filepath='.env'):
		with open(filepath, 'w') as f:
			for key, value in env_vars.items():
				f.write(f'{key}={value}\n')
	save_env_dict(env_vars, filepath='.env')
"