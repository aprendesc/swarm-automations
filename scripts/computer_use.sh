cd C:/Users/$USERNAME/Desktop/proyectos/swarm-automations
export PYTHONPATH=/c/Users/$USERNAME/Desktop/proyectos/swarm-automations:/c/Users/$USERNAME/Desktop/proyectos/eigenlib
source .venv/Scripts/activate
export PYTHONUNBUFFERED=1
python -c "
from swarmautomations.main import MainClass
from swarmautomations.config import test_config as config
config = {
  'continue_action': True,
  'instructions': input('Operator instructions: '),
  'model': 'computer-use-preview'
  }
main=MainClass(config)
main.computer_use_automation(config)
"