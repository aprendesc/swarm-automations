cd C:/Users/$USERNAME/Desktop/proyectos/swarm-automations
export PYTHONPATH=/c/Users/$USERNAME/Desktop/proyectos/swarm-automations:/c/Users/$USERNAME/Desktop/proyectos/eigenlib
source .venv/Scripts/activate
export PYTHONUNBUFFERED=1
python -c "
import time
from swarmautomations.main import NanoNetMainClass
from eigenlib.utils.nano_net import NanoNetClass
################################################################################################################
config = {
	'password':'youshallnotpass',
	'master_address':'tcp://0.0.0.0:5005'
	}
################################################################################################################
NanoNetClass.kill_processes_on_port(5005)
main=NanoNetMainClass(config)
main.launch_personal_server(config)
while True:
	time.sleep(1)
"