cd C:/Users/$USERNAME/Desktop/proyectos/swarm-automations
export PYTHONPATH=/c/Users/$USERNAME/Desktop/proyectos/swarm-automations:/c/Users/$USERNAME/Desktop/proyectos/eigenlib
source .venv/Scripts/activate
export PYTHONUNBUFFERED=1
python -c "
from swarmautomations.main import AutomationsMainClass
from swarmautomations.config import automations_test_config as config
main=AutomationsMainClass(config)
main.standby(config)
"