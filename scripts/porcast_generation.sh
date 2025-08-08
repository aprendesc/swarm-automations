cd C:/Users/$USERNAME/Desktop/proyectos/swarm-automations
export PYTHONPATH=/c/Users/$USERNAME/Desktop/proyectos/swarm-automations:/c/Users/$USERNAME/Desktop/proyectos/eigenlib
source .venv/Scripts/activate
export PYTHONUNBUFFERED=1
python -c "
import os
import pandas as pd
from swarmautomations.main import MainClass
from swarmautomations.config import active_config as config
from eigenlib.utils.project_setup import ProjectSetupClass
ProjectSetupClass(project_folder='swarm-automations')
path = 'C:/Users/AlejandroPrendesCabo/Desktop/proyectos/swarm-intelligence-project/data/raw/source_papers'
files = os.listdir(path)
print(pd.Series(files))
selection = int(input('Seleccione el paper a generar: '))
input_file = os.path.join(path, files[selection])
main=MainClass(config)
main.generate_podcast(config)
"