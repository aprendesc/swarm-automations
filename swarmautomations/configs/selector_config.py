from swarmautomations.configs.test_config import config

menu = {
    '1': 'standby',
    '2': 'call_to_notion',
    '3': 'listen_smartwatch_notes',
    '4': 'computer_use_automation',
    '5': 'youtube_to_notion',
    '6': 'sources_parser_and_summarizer',
    '7': 'podcast_generation',
    '8': 'code_interpreter',
    '9': 'intelligent_web_search',
    '10': 'google_search',
    '11': 'browse_url',
    '12': 'local_file_operations_tools',
    '13': 'get_files_map',
    '14': 'vector_database',
    '15': 'extract_info',
}

print("Aplicaciones disponibles:")
for k, v in menu.items():
    print(f"  {k}. {v}")

selection = input('Select app: ').strip()
app_name = menu.get(selection)

########################################################################################################################
# Bloques independientes por método
########################################################################################################################
if app_name == 'standby':
    config['time_interval'] = int(input('Select time_interval: '))
    pass

elif app_name == 'call_to_notion':
    # No necesita parámetros adicionales
    pass

elif app_name == 'listen_smartwatch_notes':
    #config['audio_path'] = input('Select audio_path: ')
    #config['sw_notion_page'] = input('Select sw_notion_page: ')
    pass

elif app_name == 'computer_use_automation':
    config['instructions'] = input('Select instructions: ')
    #config['model'] = input('Select model: ')
    #config['continue_action'] = input('Select continue_action: ')
    pass

elif app_name == 'youtube_to_notion':
    config['yttn_video_url'] = input('Select yttn_video_url: ')
    #config['yttn_notion_page'] = input('Select yttn_notion_page: ')
    #config['yttn_summarize'] = input('Select yttn_summarize: ')
    config['yttn_n_sections'] = input('Select yttn_n_sections: ')
    pass

elif app_name == 'sources_parser_and_summarizer':
    config['source_path_or_url'] = input('Select source_path_or_url: ')
    #config['summarizer_notion_page'] = input('Select summarizer_notion_page: ')
    config['parse'] = input('Select parse: ')
    config['summarize'] = input('Select summarize: ')
    config['n_sections'] = input('Select n_sections: ')
    config['to_notion'] = input('Select to_notion(y/n): ') == 'y'
    pass

elif app_name == 'podcast_generation':
    config['max_iter'] = input('Select max_iter: ')
    config['podcast_folder_path'] = input('Select podcast_folder_path: ')
    pass

elif app_name == 'code_interpreter':
    config['programming_language'] = input('Select programming_language: ')
    config['code'] = input('Select code: ')
    #config['interpreter_launcher'] = input('Select interpreter_launcher: ')
    #config['interpreter_cwd'] = input('Select interpreter_cwd: ')
    #config['interpreter_path_dirs'] = input('Select interpreter_path_dirs: ')
    pass

elif app_name == 'intelligent_web_search':
    config['query'] = input('Select query: ')
    config['num_results'] = input('Select num_results: ')
    config['summarize_search'] = input('Select summarize_search(y/n): ') == 'y'
    pass

elif app_name == 'google_search':
    config['query'] = input('Select query: ')
    config['num_results'] = input('Select num_results: ')
    pass

elif app_name == 'browse_url':
    config['urls'] = input('Select urls: ')
    pass

elif app_name == 'local_file_operations_tools':
    config['mode'] = input('Select mode: ')
    config['files_cwd'] = input('Select files_cwd: ')
    config['file_path'] = input('Select file_path: ')
    config['content'] = input('Select content: ')
    pass

elif app_name == 'get_files_map':
    config['map_base_path'] = input('Select map_base_path: ')
    config['map_root_dir'] = input('Select map_root_dir: ')
    pass

elif app_name == 'vector_database':
    config['vdb_mode'] = input('Select vdb_mode(fit/initialize/retrieval): ')
    config['raw_sources'] = input('Select raw_sources(list): ')
    config['vdb_name'] = input('Select vdb_name: ')
    config['vdb_chunking_threshold'] = input('Select vdb_chunking_threshold: ')
    config['lang'] = input('Select lang: ')
    config['vdb_wd'] = input('Select vdb_wd: ')
    config['query'] = input('Select query: ')
    config['top_n'] = input('Select top_n: ')
    pass

elif app_name == 'extract_info':
    #config['extraction_landing_page_id'] = input('Select extraction_landing_page_id: ')
    pass

else:
    raise ValueError('Método no soportado o selección errónea.')

print('\nConfiguración final:')
for k, v in config.items():
    print(f"{k}: {v}")
