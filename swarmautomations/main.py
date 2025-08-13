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

    def computer_use_automation(self, config):
        from eigenlib.LLM.computer_use_tools import ComputerUseClass
        ################################################################################################################
        continue_action = config['continue_action']
        instructions = config['instructions']
        model = config['model']
        ################################################################################################################
        CUA = ComputerUseClass()
        CUA.run(continue_action, instructions, model)
        return config

    def call_to_notion(self, config):
        from swarmautomations.modules.call_recording_pipeline import CallRecordingPipelineClass
        ################################################################################################################
        ################################################################################################################
        CallRecordingPipelineClass().run()
        return config

    def listen_smartwatch_notes(self, config):
        from eigenlib.audio.oai_whisper_stt import OAIWhisperSTTClass
        from eigenlib.utils.notion_utils import NotionUtilsClass
        import os
        import time

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
                        time.sleep(2)  # Pequeña pausa tras el procesamiento

                processed_files = current_files
                time.sleep(5)  # Esperar antes de la próxima comprobación

            except Exception as e:
                print(f"❌ Error durante el procesamiento: {e}")
                time.sleep(5)

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
        youtube_utils = YoutubeUtilsClass(quiet=False)
        whisper_model = OAIWhisperSTTClass()
        with tempfile.TemporaryDirectory() as tmpdir:
            result_path = youtube_utils.download_audio(video_url=video_url, output_dir=tmpdir, filename='temp_audio', compress=True, compression_level='medium')
            transcription = whisper_model.run(result_path, engine='cloud')
        print('Transcription completed')
        if summarize:
            transcription = SourceSummarizationClass().run(transcription, n_sections=int(n_sections))
            print('Summarization completed')
        NU = NotionUtilsClass()
        NU.write(page_id=notion_page, texto='* ' + transcription)
        return config

    def source_to_notion_summary(self, config):
        from swarmautomations.modules.automatic_summarizer import SourceSummarizationClass
        from eigenlib.utils.notion_utils import NotionUtilsClass
        ################################################################################################################
        source = config['source']
        notion_page = config['summarizer_notion_page']
        ################################################################################################################
        summary = SourceSummarizationClass().run(source, n_sections=2)
        NU = NotionUtilsClass()
        NU.write(page_id=notion_page, texto='* ' + summary)

    def podcast_generation(self, config):
        from swarmautomations.modules.podcast_generation import PodcastGeneration
        ################################################################################################################
        max_iter = config['max_iter']
        podcast_path = config['podcast_folder_path']
        ################################################################################################################
        PodcastGeneration().run(max_iter, podcast_path)
        return config
