hypothesis = """Automations app"""

config = {
            'hypothesis': hypothesis,

            # STANDBY
            'time_interval': 1,

            # CALL TO NOTION (pipe de llamadas grabadas)
            # No requiere parámetros adicionales

            # SMARTWATCH NOTES → NOTION
            'audio_path': 'G:/Mi unidad/utils/Easy Voice Recorder',
            'sw_notion_page': '23d2a599e98580d6b20dc30f999a1a2c',

            # COMPUTER USE AUTOMATION
            'instructions': """This is a test, make a random movement of the mouse, and then say OBJECTIVE ACCOMPLISHED to finish.""",
            'model': 'computer-use-preview',
            'continue_action': True,

            # YOUTUBE → NOTION
            'yttn_video_url': 'https://www.youtube.com/watch?v=1uX0qHQfSMg',
            'yttn_notion_page': '2432a599e985804692b7d6982895a2b2',
            'yttn_summarize': True,
            'yttn_n_sections': 5,

            # SOURCES PARSER & SUMMARIZER
            'source_path_or_url': 'https://arxiv.org/pdf/2506.21734',
            'summarizer_notion_page': '2432a599e985804692b7d6982895a2b2',
            'parse': True,
            'summarize': True,
            'n_sections': 2,
            'to_notion': True,

            # PODCAST GENERATION
            'max_iter': 15,
            'podcast_folder_path': './data/processed/podcast_pipeline_stage',

            # CODE INTERPRETER
            'programming_language': 'python',
            'code': 'print("Hola mundo!")',

            # LOCAL FILE OPERATIONS
            'mode': 'read_file',
            'file_path': './swarmautomations/main.py',
            'content': 'no_content',

            # GET FILES MAP
            'map_root_dir': './',

            # INTELLIGENT / GOOGLE WEB SEARCH
            'query': 'F22 Raptor',
            'num_results': 2,
            'summarize_search': True,
            # browse_url recibirá "urls" dinámicamente desde google_search durante los tests

            # DEF VECTOR DATABASE CREATE
            'vdb_mode': 'fit',
            'raw_sources': [],
            'seeds_chunking_threshold': 900,
            'vdb_name': 'test_VDB',
            'vdb_chunking_threshold': 150,
            'vdb_query': 'Capital de Francia',
            'lang': 'eng',
            'vdb_wd': 'C:/Users/AlejandroPrendesCabo/Desktop/proyectos/swarm-automations',

            # EXTRACT INFO
            'extraction_landing_page_id': '2522a599e985808aa4c9fbba83fe3c67',

            # DEPLOY PROJECT SERVER
            'launch_master': True,
            }

########################################################################################################################
