cd C:/Users/$USERNAME/Desktop/proyectos/swarm-automations
export PYTHONPATH=/c/Users/$USERNAME/Desktop/proyectos/swarm-automations:/c/Users/$USERNAME/Desktop/proyectos/eigenlib
source .venv/Scripts/activate
export PYTHONUNBUFFERED=1
python -c "
from eigenlib.utils.project_setup import ProjectSetupClass
from swarmautomations.main import AutomationsMainClass
from swarmautomations.config import automations_test_config as config
config['yttn_video_url'] = input('VIDEO URL:')
config['yttn_summarize'] = 'y'==input('SUMMARIZE?(y/n):')
if config['yttn_summarize']:
	config['yttn_n_sections'] = input('SUMMARIZATION SECTIONS:')
main=AutomationsMainClass(config)
main.youtube_to_notion(config)
"