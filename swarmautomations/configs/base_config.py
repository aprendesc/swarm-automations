

class Config:
    def __init__(self, hypothesis='Automations app'):
        self.hypothesis = hypothesis

    def standby(self, update=None):
        return {'time_interval': 1} | (update or {})

    def call_to_notion(self, update=None):
        return {} | (update or {})

    def smartwatch_notes(self, update=None):
        config = {
            'audio_path': 'G:/Mi unidad/utils/Easy Voice Recorder',
            'sw_notion_page': '23d2a599e98580d6b20dc30f999a1a2c',
        }
        return config | (update or {})

    def computer_use(self, update=None):
        config = {
            'instructions': 'This is a test, make a random movement of the mouse, and then say OBJECTIVE ACCOMPLISHED to finish.',
            'model': 'computer-use-preview',
            'continue_action': True,
        }
        return config | (update or {})

    def youtube_to_notion(self, update=None):
        config = {
            'yttn_video_url': 'https://www.youtube.com/watch?v=1uX0qHQfSMg',
            'yttn_notion_page': '2432a599e985804692b7d6982895a2b2',
            'yttn_summarize': True,
            'yttn_n_sections': 5,
        }
        return config | (update or {})

    def sources_parser_and_summarizer(self, update=None):
        config = {
            'source_path_or_url': 'https://arxiv.org/pdf/2506.21734',
            'summarizer_notion_page': '2432a599e985804692b7d6982895a2b2',
            'parse': True,
            'summarize': True,
            'n_sections': 2,
            'to_notion': True,
        }
        return config | (update or {})

    def podcast_generation(self, update=None):
        config = {
            'max_iter': 15,
            'podcast_folder_path': './data/processed/podcast_pipeline_stage',
        }
        return config | (update or {})

    def code_interpreter(self, update=None):
        config = {
            'programming_language': 'python',
            'code': 'print(\"Hola mundo!\")',
        }
        return config | (update or {})

    def local_file_operations(self, update=None):
        config = {
            'mode': 'read_file',
            'file_path': './swarmautomations/main.py',
            'content': 'no_content',
            'content_to_replace': None,
        }
        return config | (update or {})

    def get_files_map(self, update=None):
        config = {'map_root_dir': './'}
        return config | (update or {})

    def google_web_search(self, update=None):
        config = {
            'query': 'F22 Raptor',
            'num_results': 2
        }
        return config | (update or {})

    def vector_database(self, update=None):
        config = {
            'vdb_mode': 'fit',
            'raw_sources': [],
            'seeds_chunking_threshold': 900,
            'vdb_name': 'test_VDB',
            'vdb_chunking_threshold': 150,
            'vdb_query': 'Capital de Francia',
            'lang': 'eng',
            'vdb_wd': 'C:/Users/AlejandroPrendesCabo/Desktop/proyectos/swarm-automations',
        }
        return config | (update or {})

    def browse_url(self, update=None):
        config = {'urls': ['https://en.wikipedia.org/wiki/Lockheed_Martin_F-22_Raptor']}
        return config | (update or {})

    def extract_info(self, update=None):
        config = {
            'extraction_landing_page_id': '2522a599e985808aa4c9fbba83fe3c67'
        }
        return config | (update or {})

    def dev_tools_server(self, update=None):
        config = {
            'node_name': 'project_dev_node',
            'delay': 1,
            'password': 'internal_pass',
        }
        return config | (update or {})
