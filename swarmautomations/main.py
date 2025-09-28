from eigenlib.utils.setup import Setup

class Main:
    def __init__(self):
        Setup().init()

    def real_time_transcriptor(self, config):
        from swarmautomations.modules.real_time_transcriptor import RealTimeTranscriptor
        sample_rate = config.get('sample_rate', 48000)
        rt = RealTimeTranscriptor(sample_rate=sample_rate)
        rt.wait()

    def standby(self, config):
        from swarmautomations.modules.standby import StandbyClass
        ################################################################################################################
        time_interval = config['time_interval']
        ################################################################################################################
        monitor = StandbyClass(interval=time_interval)
        monitor.run()

    def call_to_notion(self, config):
        from swarmautomations.modules.transcriptor import Transcriptor
        ################################################################################################################
        ################################################################################################################
        app = Transcriptor(
            output_dir="./data/processed/audios",
            block_duration=120,
            sample_rate=48000,
            compression="medium",
            to_notion=True,
            notion_page_id="23d2a599e98580d6b20dc30f999a1a2c"
        )
        app.run()
        return config

    def smartwatch_notes(self, config):
        from eigenlib.audio.oai_whisper_stt import OAIWhisperSTTClass
        from eigenlib.utils.notion_io import NotionIO
        import os, time
        ################################################################################################################
        audio_path = config['audio_path']
        notion_page = config['sw_notion_page']
        ################################################################################################################
        whisper_model = OAIWhisperSTTClass()
        NM = NotionIO()
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
                        NM.write_text(page_id=notion_page, text='* ' + transcription)
                        os.remove(file_path)
                        print(f"✅ Procesado y eliminado: {f}")
                        time.sleep(2)
                processed_files = current_files
                time.sleep(5)
            except Exception as e:
                print(f"❌ Error durante el procesamiento: {e}")
                time.sleep(5)

    def computer_use_automation(self, config):
        from eigenlib.genai.tools.computer_use_tools import ComputerUseClass
        ################################################################################################################
        continue_action = config['continue_action']
        instructions = config['instructions']
        model = config['model']
        ################################################################################################################
        ComputerUseClass().run(continue_action, instructions, model)
        return config

    def youtube_to_notion(self, config):
        import tempfile
        from swarmautomations.modules.youtube_utils import YoutubeUtilsClass
        from eigenlib.audio.oai_whisper_stt import OAIWhisperSTTClass
        from eigenlib.utils.notion_io import NotionIO
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
        NotionIO().write_text(page_id=notion_page, text='* ' + transcription)
        return config

    def sources_parser_and_summarizer(self, config):
        from swarmautomations.modules.automatic_summarizer import SourceSummarizationClass
        from eigenlib.utils.notion_io import NotionIO
        from eigenlib.genai.sources_parser import SourcesParserClass
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
            NotionIO().write_text(page_id=notion_page, text='> ' + content)
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
        import subprocess
        import sys
        from io import StringIO
        ################################################################################################################
        programming_language = config['programming_language']
        code = config['code']
        ################################################################################################################
        if programming_language == 'python':
            def run_code(code):
                old_stdout = sys.stdout
                sys.stdout = buffer = StringIO()
                try:
                    exec(code)
                    return {'output': buffer.getvalue(), 'error': ''}
                except Exception as e:
                    return {'output': buffer.getvalue(), 'error': str(e)}
                finally:
                    sys.stdout = old_stdout
            config['result'] = run_code(code)
        else:
            completed = subprocess.run(code, shell=True, capture_output=True, text=True)
            config['result'] = {'output': completed.stdout, 'error': completed.stderr or None}
        return config

    def local_file_operations_tools(self, config):
        ################################################################################################################
        file_path = config['file_path']
        mode = config['mode']
        file_content = config.get('content', None)
        content_to_replace = config.get('content_to_replace', None)
        ################################################################################################################
        if mode == 'read_file':
            with open(file_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
            config['result'] = {'file_content': contenido}
        elif mode == 'write_file':
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            config['result'] = {'tool_answer': 'Content successfully written to file.'}
        elif mode == 'replace':
            with open(file_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
            if content_to_replace is None:
                config['result'] = {'tool_answer': 'No content_to_replace provided.'}
            elif contenido.find(content_to_replace) == -1:
                config['result'] = {'tool_answer': 'Content to replace not found in file.'}
            else:
                nuevo_contenido = contenido.replace(content_to_replace, file_content)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(nuevo_contenido)
                config['result'] = {'tool_answer': 'Content successfully replaced in file.'}
        return config

    def vector_database(self, config):
        from eigenlib.LLM.vector_database import VectorDatabaseClass
        from eigenlib.LLM.sources_parser import SourcesParserClass
        from eigenlib.utils.data_io import DataIO
        import os
        import copy
        ############################################################################################################
        mode = config['vdb_mode']
        vdb_wd = config['vdb_wd']
        ############################################################################################################
        old_wd = copy.deepcopy(os.getcwd())
        os.chdir(vdb_wd)
        if mode == 'initialize':
            VDB_name = config['vdb_name']
            ############################################################################################################
            self.VDB = VectorDatabaseClass(content_feature='steering')
            self.VDB.initialize(vdb_name=VDB_name)
        elif mode == 'fit':
            ############################################################################################################
            raw_sources = config['raw_sources']
            lang = config['lang']
            VDB_name = config['vdb_name']
            vdb_chunking_threshold = config['vdb_chunking_threshold']
            ############################################################################################################
            df = SourcesParserClass().run_batch(raw_sources, lang=lang)
            #INDEXATION
            self.VDB = VectorDatabaseClass(content_feature='steering')
            self.VDB.initialize()
            source_df = self.VDB.create(df['content'].sum(), separator='.', create_vectors=True, chunking_threshold=vdb_chunking_threshold)
            DataIO().write(path=os.path.join(os.environ['PROCESSED_DATA_PATH'], VDB_name + '.pkl'), data=source_df)
        elif mode == 'retrieval':
            if not hasattr(self, "VDB"):
                VDB_name = config['vdb_name']
                ############################################################################################################
                self.VDB = VectorDatabaseClass(content_feature='steering')
                self.VDB.initialize(vdb_name=VDB_name)
            ############################################################################################################
            query = config.get('query', '')
            top_n = int(config.get('top_n', 5))
            ############################################################################################################
            retrieved_text = self.VDB.get(query=query, top_n=top_n)
            config['result'] = {'sources': retrieved_text}
        os.chdir(old_wd)
        return config

    def extract_info(self, config):
        import threading
        import time
        from pynput import keyboard as kb
        import pyperclip
        from eigenlib.utils.notion_io import NotionIO
        ############################################################################################################
        page_id = config.get('extraction_landing_page_id')
        run_in_background = bool(config.get('run_in_background', False))
        NU = NotionIO()
        CTRL_KEYS = {kb.Key.ctrl, kb.Key.ctrl_l, kb.Key.ctrl_r}
        ANGLE_KEY_CHAR = '<'
        ANGLE_KEY_VK = 226  # VK_OEM_102 en Windows
        ############################################################################################################
        def _copy_selected():
            controller = kb.Controller()
            controller.press(kb.Key.ctrl)
            controller.press('c')
            controller.release('c')
            controller.release(kb.Key.ctrl)
            time.sleep(0.06)
            return pyperclip.paste().strip()

        def _listener_worker():
            print("🟢 Listener activo – pulsa Ctrl+< para enviar selección a Notion.")
            ctrl_pressed = False

            def on_press(key):
                nonlocal ctrl_pressed
                if key in CTRL_KEYS:
                    ctrl_pressed = True
                    return

                if not ctrl_pressed:
                    return

                # — Detectamos la tecla < —
                is_angle_char = isinstance(key, kb.KeyCode) and key.char == ANGLE_KEY_CHAR
                is_angle_vk = getattr(key, 'vk', None) == ANGLE_KEY_VK
                if is_angle_char or is_angle_vk:
                    texto = _copy_selected()
                    if texto:
                        try:
                            NU.write_text(page_id=page_id, text=texto)
                            print(f"✅ Enviado a Notion ({len(texto)} car.).")
                        except Exception as e:
                            print(f"❌ Error al enviar a Notion: {e}")
                    else:
                        print("ℹ️  Portapapeles vacío – nada que enviar.")

            def on_release(key):
                nonlocal ctrl_pressed
                if key in CTRL_KEYS:
                    ctrl_pressed = False

            with kb.Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()

        if run_in_background:
            thread = threading.Thread(target=_listener_worker, daemon=False)
            thread.start()
            config['result'] = {'listener_started': True, 'background': True, 'thread': thread}
        else:
            _listener_worker()
            config['result'] = {'listener_started': True, 'background': False}
        return config

    def serving(self, config):
        from eigenlib.utils.network_io import NetworkIO
        import time
        ################################################################################################################
        def serving_method(method, config):
            return getattr(self, method)(config)
        MASTER_ADDRESS = config['master_address']
        node_name = config['node_name']
        delay = config['delay']
        password = config['password']
        NetworkIO().launch_master(address=MASTER_ADDRESS, password=password)
        ################################################################################################################
        NetworkIO(verbose=True).launch_node(node_name=node_name, master_address=MASTER_ADDRESS, node_method=serving_method, password=password, delay=delay)
        while True:
            time.sleep(10)
        return config

    def call(self, config):
        from eigenlib.utils.network_io import NetworkIO
        ################################################################################################################
        MASTER_ADDRESS = config['master_address']
        client_name = config['client_name']
        delay = config['delay']
        password = config['password']
        target_node = config['target_node']
        payload = config['payload']
        ################################################################################################################
        client = NetworkIO()
        client.launch_node(node_name=client_name, master_address=MASTER_ADDRESS, node_method=lambda: "OK", delay=delay, password=password)
        resultado = client.call(target_node=target_node, payload=payload)
        client.stop()
        config['result'] = resultado
        print(resultado)
        return config


if __name__ == "__main__":
    import os
    from swarmautomations.configs.base_config import Config
    os.environ['REPO_FOLDER'] = 'swarm-automations'
    main = Main()
    config = Config()
    #main.standby(config.standby())
    #main.real_time_transcriptor(config.real_time_transcriptor())
    #main.call_to_notion(config.call_to_notion())
    #main.smartwatch_notes(config.smartwatch_notes())
    #main.computer_use_automation(config.computer_use_automations())
    #main.youtube_to_notion(config.youtube_to_notion())
    #main.sources_parser_and_summarizer(config.sources_parser_and_summarizer())
    #main.podcast_generation(config.podcast_generation())
    #main.code_interpreter(config.code_interpreter())
    #main.local_file_operations_tools(config.local_file_operations_tools())
    #main.get_files_map(config.get_files_map())
    #output_cfg = main.web_search(config.web_search())
    #main.vector_database(config.vector_database())
    #main.browse_url(config.browse_url())
    #main.extract_info(config.extract_info())
    #main.dev_tools_server(config.dev_tools_server())
    #main.serving(config.serving())
    #main.call(config.call())
    #print(output_cfg)







