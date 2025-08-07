cd C:/Users/$USERNAME/Desktop/proyectos/swarm-automations
export PYTHONPATH=/c/Users/$USERNAME/Desktop/proyectos/swarm-automations:/c/Users/$USERNAME/Desktop/proyectos/eigenlib
source .venv/Scripts/activate
export PYTHONUNBUFFERED=1
python -c "
from swarmautomations.main import MainClass
from swarmautomations.config import test_config as config
config['yttn_video_url'] = input('VIDEO URL:')
config['yttn_summarize'] = 'y'==input('SUMMARIZE?(y/n):')
if config['yttn_summarize']:
	config['yttn_n_sections'] = input('SUMMARIZATION SECTIONS:')
main=MainClass(config)
main.youtube_to_notion(config)
"