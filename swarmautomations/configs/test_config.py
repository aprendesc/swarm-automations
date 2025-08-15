
########################################################################################################################
hypothesis = """Automations app"""
config = {
            'hypothesis': hypothesis,
            # STANDNBY
            'time_interval': 1,

            #COMPUTER USE
            'instructions': """This is a test, make a random movement of the mouse, and then say OBJECTIVE ACCOMPLISGED to finish.""",
            'model': "computer-use-preview",
            'continue_action': True,

            #CALL TO NOTION

            #SMARTWATCH AUDIO TO NOTION
            'audio_path': 'G:/Mi unidad/utils/Easy Voice Recorder',
            'sw_notion_page': '23d2a599e98580d6b20dc30f999a1a2c',

            # YOUTUBE TO NOTION
            'yttn_video_url': 'https://www.youtube.com/watch?v=1uX0qHQfSMg',
            'yttn_notion_page': '2432a599e985804692b7d6982895a2b2',
            'yttn_summarize': True,
            'yttn_n_sections': 5,

            # sources_parser_and_summarizer
            'source': 'https://arxiv.org/pdf/2506.21734',
            'n_sections': 2,
            'parse': True,
            'summarize': True,
            'to_notion': True,
            'summarizer_notion_page': '2432a599e985804692b7d6982895a2b2',

            # GENERATE_PODCAST
            'max_iter': 15,
            'podcast_folder_path': './data/processed/podcast_pipeline_stage',

            #CODE INTERPRETER
            'programming_language': 'python',
            'code': 'print("Hello World")',

            #INTELLIGENT WEB SEARCH
            'query': 'F22 Raptor',
            'num_results': 2,
            'summarize_search': True,

            #GET PROJECT MAP
            'base_path': './',
            'root_dir': 'swarmautomations',
        }

########################################################################################################################
