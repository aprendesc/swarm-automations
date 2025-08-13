from swarmautomations.main import MainClass
from swarmautomations.configs.test_config import test_config as config

class CLI:
    def __init__(self):
        print("""

██████╗░██████╗░░█████╗░░░░░░██╗███████╗░█████╗░████████╗  ░█████╗░██╗░░░░░██╗
██╔══██╗██╔══██╗██╔══██╗░░░░░██║██╔════╝██╔══██╗╚══██╔══╝  ██╔══██╗██║░░░░░██║
██████╔╝██████╔╝██║░░██║░░░░░██║█████╗░░██║░░╚═╝░░░██║░░░  ██║░░╚═╝██║░░░░░██║
██╔═══╝░██╔══██╗██║░░██║██╗░░██║██╔══╝░░██║░░██╗░░░██║░░░  ██║░░██╗██║░░░░░██║
██║░░░░░██║░░██║╚█████╔╝╚█████╔╝███████╗╚█████╔╝░░░██║░░░  ╚█████╔╝███████╗██║
╚═╝░░░░░╚═╝░░╚═╝░╚════╝░░╚════╝░╚══════╝░╚════╝░░░░╚═╝░░░  ░╚════╝░╚══════╝╚═╝
░╚════╝░╚══════╝╚═╝ 
                    """)
        self.main = MainClass(config)

    def run(self):
        while True:
            print("""
========================================================================================================================
""")

            # MENU
            menu_1 = """
1- Standby
2- Computer use
3- Call To Notion
4- Listen Smartwatch Notes
5- Youtube to notion
6- Source to notion
7- Podcast Generation


Select a method: """
            method = input(menu_1)

            # TREE
            if method == '1':
                self.main.standby(config)
            elif method == '2':
                config['instructions'] = input('Instructions for the automation: ')
                self.main.computer_use_automation(config)
            elif method == '3':
                self.main.call_to_notion(config)
            elif method == '4':
                self.main.listen_smartwatch_notes(config)
            elif method == '5':
                config['yttn_video_url'] = input('Video URL:')
                config['yttn_summarize'] = input('Summarize?(y/n):') == 'y'
                if config['yttn_summarize']:
                    config['yttn_n_sections'] = int(input('Number of summarizing section:'))
                self.main.youtube_to_notion(config)
            elif method == '6':
                self.main.source_to_notion_summary(config)
            elif method == '7':
                config['max_iter'] = input('Max iter: ')
                self.main.podcast_generation(config)

if __name__ == "__main__":
    CLI().run()
