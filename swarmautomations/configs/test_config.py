hypothesis = """Automations app"""

standby_config = {
            'time_interval': 1,
}

call_to_notion_config = {

            }

smartwatch_notes_config = {
    'audio_path': 'G:/Mi unidad/utils/Easy Voice Recorder',
    'sw_notion_page': '23d2a599e98580d6b20dc30f999a1a2c',
}

computer_use_config = {
    'instructions': """This is a test, make a random movement of the mouse, and then say OBJECTIVE ACCOMPLISHED to finish.""",
    'model': 'computer-use-preview',
    'continue_action': True,
}

youtube_to_notion_config = {
    'yttn_video_url': 'https://www.youtube.com/watch?v=1uX0qHQfSMg',
    'yttn_notion_page': '2432a599e985804692b7d6982895a2b2',
    'yttn_summarize': True,
    'yttn_n_sections': 5,
}

sources_parser_config = {
    'source_path_or_url': 'https://arxiv.org/pdf/2506.21734',
    'summarizer_notion_page': '2432a599e985804692b7d6982895a2b2',
    'parse': True,
    'summarize': True,
    'n_sections': 2,
    'to_notion': True,
}

podcast_generation_config = {
    'max_iter': 15,
    'podcast_folder_path': './data/processed/podcast_pipeline_stage',
}

code_interpreter_config = {
    'programming_language': 'python',
    'code': 'print("Hola mundo!")',
}

local_file_operations_config = {
        'mode': 'read_file',
        'file_path': './swarmautomations/main.py',
        'content': 'no_content',
        'content_to_replace': None,
    }

get_files_map_config = {
    'map_root_dir': './',
}

google_web_search_config = {
    'query': 'F22 Raptor',
    'num_results': 2,
}

vdb_create_config = {
    'vdb_mode': 'fit',
    'raw_sources': [],
    'seeds_chunking_threshold': 900,
    'vdb_name': 'test_VDB',
    'vdb_chunking_threshold': 150,
    'vdb_query': 'Capital de Francia',
    'lang': 'eng',
    'vdb_wd': 'C:/Users/AlejandroPrendesCabo/Desktop/proyectos/swarm-automations',
}

browser_url_config = {
    'urls': []
}

extract_info_config = {
    'extraction_landing_page_id': '2522a599e985808aa4c9fbba83fe3c67',
}

dev_tools_server_config = {
    'launch_master': True,
    'node_name': 'project_dev_node',
    'node_delay': 1,
}

config = standby_config | call_to_notion_config | smartwatch_notes_config | computer_use_config
config = config | youtube_to_notion_config | sources_parser_config | podcast_generation_config
config = config | podcast_generation_config | code_interpreter_config | local_file_operations_config
config = config | get_files_map_config | google_web_search_config | vdb_create_config
config = config | browser_url_config | extract_info_config | dev_tools_server_config
########################################################################################################################
