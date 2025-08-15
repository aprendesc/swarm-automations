
apps = {'1': 'standby',
        '2': 'call_to_notion',
        '3': 'listen_smartwatch_notes',
        '4': 'computer_use_automation',
        '5': 'youtube_to_notion',
        '6': 'sources_parser_and_summarizer',
        '7': 'podcast_generation',
        }
print("""
{'1': 'standby',
        '2': 'call_to_notion',
        '3': 'listen_smartwatch_notes',
        '4': 'computer_use_automation',
        '5': 'youtube_to_notion',
        '6': 'sources_parser_and_summarizer',
        '7': 'podcast_generation',
        }
""")
sel_n = input('Select app config: ')
sel_app = apps[sel_n]

if sel_app == 'standby':
    config = {
        'time_interval': 1,
        }

elif sel_app == 'call_to_notion':
    config = {}

elif sel_app == 'listen_smartwatch_notes':
    config = {
        'audio_path': 'G:/Mi unidad/utils/Easy Voice Recorder',
        'sw_notion_page': '23d2a599e98580d6b20dc30f999a1a2c',
    }

elif sel_app == 'youtube_to_notion':
    url = input('URL: ')
    summarize = input('Summarize? (y/n): ')=='y'
    if summarize:
        n_sections = input('Select n sections: ')
    else:
        n_sections = None
    config = {
        'yttn_video_url': url,
        'yttn_notion_page': '2432a599e985804692b7d6982895a2b2',
        'yttn_summarize': True,
        'yttn_n_sections': n_sections,
        }

elif sel_app == 'sources_parser_and_summarizer':
    source = input('Introduce source:')
    summarize = input('Summarize? (y/n): ')=='y'
    if summarize:
        n_sections = input('Select n sections: ')
    else:
        n_sections = None
    to_notion = input('Send to notion?(y/n)')=='y'
    config = {
        'parse': True,
        'to_notion': to_notion,
        'summarize': summarize,
        'source': source,
        'n_sections': n_sections,
        'summarizer_notion_page': '2432a599e985804692b7d6982895a2b2',
    }

elif sel_app == 'podcast_generation':
    config = {
            'max_iter': 15,
            'podcast_folder_path': './data/processed/podcast_pipeline_stage',
        }

########################################################################################################################
