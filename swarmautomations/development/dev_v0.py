
from swarmautomations.main import Main
from swarmautomations.configs.base_config import Config

if __name__ == "__main__":
    import os
    os.environ['REPO_FOLDER'] = 'swarm-automations'
    Main().podcast_generation(Config().podcast_generation())
