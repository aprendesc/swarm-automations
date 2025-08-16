class MainClass():
    def __init__(self, config):
        pass

    """Automations"""
    def standby(self, config):
        from swarmautomations.modules.standby import StandbyClass
        ################################################################################################################
        time_interval = config['time_interval']
        ################################################################################################################
        monitor = StandbyClass(interval=time_interval, radius=50, steps=64)
        monitor.run()

    def call_to_notion(self, config):
        from swarmautomations.modules.call_recording_pipeline import CallRecordingPipelineClass
        ################################################################################################################
        ################################################################################################################
        CallRecordingPipelineClass().run()
        return config

    def listen_smartwatch_notes(self, config):
        from eigenlib.audio.oai_whisper_stt import OAIWhisperSTTClass
        from eigenlib.utils.notion_utils import NotionUtilsClass
        import os, time
        ################################################################################################################
        audio_path = config['audio_path']
        notion_page = config['sw_notion_page']
        ################################################################################################################
        whisper_model = OAIWhisperSTTClass()
        NU = NotionUtilsClass()
        print(f"📡 Monitoreando carpeta: {audio_path}")
        processed_files = set()
        while True:
            try:
                current_files = set(os.listdir(audio_path))
                new_files = current_files - processed_files
                for f in new_files:
                    file_path = os.path.join(audio_path, f)
                    if os.path.isfile(file_path):
                        print(f"🎙️  Nuevo archivo detectado: {f}")
                        transcription = whisper_model.run(file_path, engine='cloud')
                        NU.write(page_id=notion_page, texto='* ' + transcription)
                        os.remove(file_path)
                        print(f"✅ Procesado y eliminado: {f}")
                        time.sleep(2)
                processed_files = current_files
                time.sleep(5)
            except Exception as e:
                print(f"❌ Error durante el procesamiento: {e}")
                time.sleep(5)

    def computer_use_automation(self, config):
        from eigenlib.LLM.computer_use_tools import ComputerUseClass
        ################################################################################################################
        continue_action = config['continue_action']
        instructions = config['instructions']
        model = config['model']
        ################################################################################################################
        ComputerUseClass().run(continue_action, instructions, model)
        return config

    def youtube_to_notion(self, config):
        import tempfile
        from eigenlib.utils.youtube_utils import YoutubeUtilsClass
        from eigenlib.audio.oai_whisper_stt import OAIWhisperSTTClass
        from eigenlib.utils.notion_utils import NotionUtilsClass
        from swarmautomations.modules.automatic_summarizer import SourceSummarizationClass
        ################################################################################################################
        video_url = config['yttn_video_url']
        notion_page = config['yttn_notion_page']
        summarize = config['yttn_summarize']
        n_sections = config['yttn_n_sections']
        ################################################################################################################
        yt = YoutubeUtilsClass(quiet=False)
        whisper_model = OAIWhisperSTTClass()
        with tempfile.TemporaryDirectory() as tmpdir:
            result_path = yt.download_audio(video_url=video_url, output_dir=tmpdir, filename='temp_audio', compress=True, compression_level='medium')
            transcription = whisper_model.run(result_path, engine='cloud')
        if summarize:
            transcription = SourceSummarizationClass().run(transcription, n_sections=int(n_sections))
        NotionUtilsClass().write(page_id=notion_page, texto='* ' + transcription)
        return config

    def sources_parser_and_summarizer(self, config):
        from swarmautomations.modules.automatic_summarizer import SourceSummarizationClass
        from eigenlib.utils.notion_utils import NotionUtilsClass
        from eigenlib.LLM.sources_parser import SourcesParserClass
        ################################################################################################################
        source_path_or_url = config['source_path_or_url']
        notion_page = config['summarizer_notion_page']
        parse = config['parse']
        summarize = config['summarize']
        n_sections = config['n_sections']
        to_notion = config['to_notion']
        ################################################################################################################
        result_dict = {'content': 'no source', 'succesfully_sent_to_notion': False}
        content = ''
        if parse:
            content = SourcesParserClass().run(source_path_or_url)
            source_path_or_url = content
            result_dict['content'] = content
        if summarize:
            content = SourceSummarizationClass().run(source_path_or_url, n_sections=n_sections)
            result_dict['content'] = content
        if to_notion:
            NotionUtilsClass().write(page_id=notion_page, texto='> ' + content)
            result_dict['succesfully_sent_to_notion'] = True
        config['result'] = result_dict
        return config

    def podcast_generation(self, config):
        from swarmautomations.modules.podcast_generation import PodcastGeneration
        ################################################################################################################
        max_iter = config['max_iter']
        podcast_path = config['podcast_folder_path']
        ################################################################################################################
        PodcastGeneration().run(max_iter, podcast_path)
        return config

    def code_interpreter(self, config):
        from swarmautomations.modules.code_interpreter import CodeInterpreter
        ################################################################################################################
        interpreter_launcher = config['interpreter_launcher']
        interpreter_cwd = config['interpreter_cwd']
        interpreter_path_dirs = config['interpreter_path_dirs']
        programming_language = config['programming_language']
        code = config['code']
        ################################################################################################################
        cit = CodeInterpreter(interpreter_launcher, interpreter_path_dirs, cwd=interpreter_cwd)
        config['result'] = cit.run(programming_language=programming_language, code=code)
        return config

    def intelligent_web_search(self, config):
        from swarmautomations.modules.intelligent_web_search import IntelligentWebSearch
        ################################################################################################################
        query = config['query']
        num_results = config['num_results']
        summarize = config['summarize_search']
        ################################################################################################################
        config['result'] = IntelligentWebSearch().run(query, num_results, summarize)
        return config

    def google_search(self, config):
        from googlesearch import search
        ################################################################################################################
        query = config['query']
        num_results = config['num_results']
        ################################################################################################################
        config['result'] = {'urls': list(search(query, num_results=num_results))}
        return config

    def browse_url(self, config):
        from swarmautomations.modules.intelligent_web_search import IntelligentWebSearch
        from eigenlib.utils.parallel_utils import ParallelUtilsClass
        ################################################################################################################
        urls = config['urls']
        query = config['query']
        summarize = config['summarize_search']
        ################################################################################################################
        if isinstance(urls, str):
            urls = [urls]
        IWS = IntelligentWebSearch()
        IWS.summarize = summarize
        IWS.model = 'gpt-5-nano'
        result = ParallelUtilsClass().run_in_parallel(IWS._url_to_summary, {'query': query}, {'url': urls}, n_threads=len(urls), use_processes=False)
        config['result'] = {'summary': '\n'.join(result)}
        return config

    def local_file_operations_tools(self, config):
        import os, copy
        ################################################################################################################
        file_path = config['file_path']
        base_path = config['local_base_path']
        mode = config['mode']
        file_content = config.get('content', None)
        ################################################################################################################
        old_wd = copy.deepcopy(os.getcwd())
        os.chdir(base_path)
        if mode == 'read_file':
            with open(file_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
            config['result'] = {'file_content': contenido}
        elif mode == 'write_file':
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            config['result'] = {'tool_answer': 'Content successfully written to file.'}
        os.chdir(old_wd)
        return config

    def get_files_map(self, config):
        import os, copy
        ################################################################################################################
        map_base_path = config['map_base_path']
        map_root_dir = config['map_root_dir']
        ################################################################################################################
        def project_map(root_dir, excluded=['__', '.venv', 'git', '.env', '.pytest', '.idea']):
            map = []
            for root, _, files in os.walk(root_dir):
                for name in files:
                    file_path = os.path.join(root, name)
                    if any(sub in file_path for sub in excluded):
                        continue
                    map.append(file_path)
            return map
        old_wd = copy.deepcopy(os.getcwd())
        os.chdir(map_base_path)
        map = project_map(map_root_dir)
        os.chdir(old_wd)
        config['result'] = {'files_map': map}
        return config