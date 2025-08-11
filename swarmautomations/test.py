import unittest
from eigenlib.utils.project_setup import ProjectSetupClass
ProjectSetupClass(project_folder='swarm-automations', test_environ=True)

########################################################################################################################
"""SWARM AUTOMATIONS TESTS"""
########################################################################################################################

class UnitTestMainClass(unittest.TestCase):
    def setUp(self):
        from eigenlib.utils.testing_utils import TestingUtilsClass
        from swarmautomations.main import MainClass
        ################################################################################################################
        self.test_df, self.model, self.image, self.texto = TestingUtilsClass().get_dummy_data()
        self.main = MainClass({})

    def test_computer_use_automation(self):
        ################################################################################################################
        config = {
            'instructions': """This is a test, just move a bit the mouse and finish saying OBJECTIVE ACCOMPLISHED""",
            'model': "computer-use-preview",
            'continue_action': False,
        }
        ################################################################################################################
        self.main.computer_use_automation(config)

    def test_standby(self):
        import threading
        import time
        ################################################################################################################
        config = {'time_interval': 1}
        ################################################################################################################        standby_thread = threading.Thread(target=self.main.standby,
        standby_thread = threading.Thread(target=self.main.standby, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(3)

    def test_call_to_notion(self):
        import threading
        import time
        ################################################################################################################
        config = {}
        ################################################################################################################        standby_thread = threading.Thread(target=self.main.standby,
        standby_thread = threading.Thread(target=self.main.call_to_notion, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(3)

    def test_listen_smartwatch_notes(self):
        import threading
        import time
        ################################################################################################################
        config = {
            'audio_path': 'G:/Mi unidad/utils/Easy Voice Recorder',
            'sw_notion_page': '23d2a599e98580d6b20dc30f999a1a2c'
        }
        ################################################################################################################        standby_thread = threading.Thread(target=self.main.standby,
        standby_thread = threading.Thread(target=self.main.listen_smartwatch_notes, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(3)

    def test_youtube_to_notion(self):
        import threading
        import time
        ################################################################################################################
        config = {
            'yttn_video_url': 'https://www.youtube.com/watch?v=1uX0qHQfSMg',
            'yttn_notion_page': '2432a599e985804692b7d6982895a2b2',
            'yttn_summarize': True,
            'yttn_n_sections': 5,
        }
        ################################################################################################################        standby_thread = threading.Thread(target=self.main.standby,
        standby_thread = threading.Thread(target=self.main.youtube_to_notion, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(3)

    def test_source_to_notion_summary(self):
        import threading
        import time
        ################################################################################################################
        config = {
            'source': 'Hola Mundo',
            'n_sections': 2,
            'summarizer_notion_page': '2432a599e985804692b7d6982895a2b2',
        }
        ################################################################################################################        standby_thread = threading.Thread(target=self.main.standby,
        standby_thread = threading.Thread(target=self.main.source_to_notion_summary, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(3)

    @unittest.skip("Class not functional")
    def test_podcast_generation(self):
        import threading
        import time
        ################################################################################################################
        config = {
            'max_iter': 15,
            'podcast_folder_path': './data/processed/podcast_pipeline_stage',
        }
        ################################################################################################################        standby_thread = threading.Thread(target=self.main.standby,
        standby_thread = threading.Thread(target=self.main.podcast_generation, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(3)

    def test_launch_personal_server(self):
        import threading
        import time
        ################################################################################################################
        config = {
            'master_address': 'tcp://localhost:5005',
            'password': 'test_pass',
        }
        ################################################################################################################        standby_thread = threading.Thread(target=self.main.standby,
        standby_thread = threading.Thread(target=self.main.launch_personal_server, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(3)

    def test_launch_personal_server_node(self):
        import threading
        import time
        ################################################################################################################
        config = {
            'node_name': 'test_node',
            'node_method': lambda a, b: a + b,
            'delay': 1,
        }
        ################################################################################################################        standby_thread = threading.Thread(target=self.main.standby,
        standby_thread = threading.Thread(target=self.main.launch_personal_server_node, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(3)

    def test_call_personal_server_node(self):
        import threading
        import time
        ################################################################################################################
        config_server = {
            'master_address': 'tcp://localhost:5005',
            'password': 'test_pass',
        }
        config_node = {
            'master_address': 'tcp://localhost:5005',
            'node_name': 'test_node',
            'password': 'test_pass',
            'node_method': lambda a, b: a + b,
            'delay': 1,
        }
        config_client = {
            'master_address': 'tcp://localhost:5005',
            'address_node': 'test_node',
            'password': 'test_pass',
            'payload': {'a': 1, 'b':2}
        }
        ################################################################################################################        standby_thread = threading.Thread(target=self.main.standby,
        standby_thread_1 = threading.Thread(target=self.main.launch_personal_server, args=(config_server,), daemon=True)
        standby_thread_1.start()
        standby_thread_2 = threading.Thread(target=self.main.launch_personal_server_node, args=(config_node,), daemon=True)
        standby_thread_2.start()
        standby_thread_3 = threading.Thread(target=self.main.launch_personal_server, args=(config_client,), daemon=True)
        standby_thread_3.start()
        time.sleep(3)
        standby_thread_1.join(timeout=0.1)
        standby_thread_2.join(timeout=0.1)
        standby_thread_3.join(timeout=0.1)

class UnitTestModulesClass(unittest.TestCase):
    def setUp(self):
        import os
        from eigenlib.utils.testing_utils import TestingUtilsClass, module_test_coverage
        ################################################################################################################
        module_test_coverage(os.environ['PROJECT_NAME'] + '.modules', self)
        self.test_df, self.model, self.image, self.texto = TestingUtilsClass().get_dummy_data()

    def test_automatic_summarizer(self):
        from swarmautomations.modules.automatic_summarizer import SourceSummarizationClass
        ################################################################################################################
        source = """Lorem ipsum dolor sit amet, 
        consectetur adipiscing elit, 
        sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
        Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""
        ################################################################################################################
        ssc = SourceSummarizationClass()
        ssc.run(source, n_sections=2, max_len=350000, overlap=25000, temperature=1, model='gpt-4.1')

    def test_call_recording_pipeline(self):
        import threading
        import time
        from swarmautomations.modules.call_recording_pipeline import CallRecordingPipelineClass
        ################################################################################################################
        ################################################################################################################
        def aux_fun():
            CallRecordingPipelineClass().run()
        standby_thread = threading.Thread(target=aux_fun, daemon=True)
        standby_thread.start()
        time.sleep(3)

    def test_standby(self):
        import threading
        import time
        from swarmautomations.modules.standby import StandbyClass
        ################################################################################################################
        config = {'interval': 1}
        ################################################################################################################
        def aux_fun(config):
            StandbyClass(**config).run()
        standby_thread = threading.Thread(target=aux_fun, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(3)

########################################################################################################################
"""EIGENLIB TESTS"""
########################################################################################################################

class UnitTestAudioClass(unittest.TestCase):

    def setUp(self):
        import sys
        from eigenlib.utils.testing_utils import TestingUtilsClass, module_test_coverage
        ################################################################################################################
        sys.path.extend(['C:\\Users\\AlejandroPrendesCabo\\Desktop\\proyectos\\eigenlib'])
        module_test_coverage('eigenlib.audio', self)
        self.test_df, self.model, self.image, self.texto = TestingUtilsClass().get_dummy_data()

    def test_audio_utils_class(self):
        import tempfile, os
        from eigenlib.audio.audio_utils import AudioUtilsClass
        ################################################################################################################
        ################################################################################################################
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        tmp_path = tmp.name
        tmp.close()
        audio_utils = AudioUtilsClass(frequency=44100, size=-16, channels=2, buffer=512)
        wav_bytes = audio_utils.record_audio(duration=2)
        audio_utils.save_audio(audio_bytes=wav_bytes, audio_path=tmp_path)
        wav_bytes_loaded = audio_utils.load_audio(audio_path=tmp_path)
        audio_utils.play_audio(audio_bytes=wav_bytes_loaded)
        os.unlink(tmp_path)

    def test_oai_whisper_stt_class(self):
        import tempfile, os
        from eigenlib.audio.audio_utils import AudioUtilsClass
        from eigenlib.audio.oai_whisper_stt import OAIWhisperSTTClass
        ################################################################################################################
        ################################################################################################################
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        audio_path = tmp.name
        tmp.close()
        audio_utils = AudioUtilsClass(frequency=44100, size=-16, channels=2, buffer=512)
        wav_bytes = audio_utils.record_audio(duration=2)
        audio_utils.save_audio(audio_bytes=wav_bytes, audio_path=audio_path)
        #---------------------------------------------------------------------------------------------------------------
        stt = OAIWhisperSTTClass()
        transcription = stt.run(audio_path=audio_path, engine='cloud')
        print(transcription)
        os.unlink(audio_path)

    def test_audio_mixer_recorder(self):
        import time, tempfile, os
        from eigenlib.audio.audio_mixer_recorder import AudioMixerRecorder
        from eigenlib.audio.audio_utils import AudioUtilsClass
        ################################################################################################################
        ################################################################################################################
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        p = tmp.name
        tmp.close()
        rec = AudioMixerRecorder(archivo_salida=p, tasa_muestreo=48000, volumen_loopback=0.5, volumen_microfono=0.5)
        rec.start()
        time.sleep(5)
        rec.stop()
        au = AudioUtilsClass()
        b = au.load_audio(audio_path=p.replace('.wav', '.flac'))
        au.play_audio(audio_bytes=b)
        os.unlink(p.replace('.wav', '.flac'))

    def test_oai_tts_model_class(self):
        import tempfile, os
        from eigenlib.audio.oai_tts import OAITTSModelClass
        from eigenlib.audio.audio_utils import AudioUtilsClass
        ################################################################################################################
        ################################################################################################################
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        path = tmp.name
        tmp.close()
        OAITTSModelClass(voice='alloy').run(text="Hola, este es un test de síntesis TTS.", path=path)
        au = AudioUtilsClass()
        au.play_audio(audio_bytes=au.load_audio(audio_path=path))
        os.unlink(path)

class UnitTestImageClass(unittest.TestCase):

    def setUp(self):
        from eigenlib.utils.testing_utils import TestingUtilsClass, module_test_coverage
        ################################################################################################################
        module_test_coverage('eigenlib.image', self)
        self.test_df, self.model, self.image, self.texto = TestingUtilsClass().get_dummy_data()

    @unittest.skip("Class not functional")
    def test_clip_embedding_model(self):
        import tempfile, os, torch
        from PIL import Image
        from eigenlib.image.clip_embedding_model import ClipEmbeddingsModel
        tmp = tempfile.TemporaryDirectory()
        p1, p2 = f"{tmp.name}/i1.jpg", f"{tmp.name}/i2.jpg"
        Image.new('RGB', (224, 224), (255, 0, 0)).save(p1)
        Image.new('RGB', (224, 224), (0, 255, 0)).save(p2)
        m = ClipEmbeddingsModel()
        m.initialize(model_repo_name="openai/clip-vit-base-patch32", processor_repo_name="openai/clip-vit-base-patch32")
        img_emb = m.predict(input_data=[p1, p2], prediction_type="image")
        txt_emb = m.predict(input_data=["red square", "green square"], prediction_type="text")
        print(m.get_similarity(img_emb[0].unsqueeze(0), txt_emb))
        tmp.cleanup()

    def test_dalle_model(self):
        import tempfile, os, cv2
        import numpy as np
        from eigenlib.image.dalle_model import DalleModelClass
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        path = tmp.name
        tmp.close()
        img = DalleModelClass().predict(prompt="A cute cat sitting on a chair")
        img.save(path)
        cv2.imshow('img', cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
        cv2.waitKey(2000)
        cv2.destroyAllWindows()
        os.unlink(path)

class UnitTesLLMClass(unittest.TestCase):
    def setUp(self):
        from eigenlib.utils.testing_utils import TestingUtilsClass, module_test_coverage
        ################################################################################################################
        module_test_coverage('eigenlib.LLM', self)
        self.test_df, self.model, self.image, self.texto = TestingUtilsClass().get_dummy_data()

    def test_base_agent_tools(self):
        import json
        from eigenlib.LLM.base_agent_tools import VDBToolClass
        ################################################################################################################
        tool = VDBToolClass(vdb_name="test_vdb", use_cloud=False)
        tool.initialize()
        res = tool.run(answer_trial="Paris is the capital of France", search_terms="Eiffel Tower")
        print(json.loads(res))

    def test_computer_use_tools(self):
        from eigenlib.LLM.computer_use_tools import ComputerUseClass
        ################################################################################################################
        config = {
            'instructions': """As test, move the mouse to the up left corner and finish your work. Say OBJECTIVE ACCOMPLISHED when you finish.""",
            'model': "computer-use-preview",
            'continue_action': True,
        }
        ################################################################################################################
        CUA = ComputerUseClass()
        CUA.run(**config)

    def test_dataset_autolabeling(self):
        import types, pandas as pd, os, time
        from eigenlib.LLM.dataset_autolabeling import DatasetAutolabelingClass as DL
        import eigenlib.LLM.dataset_autolabeling as _m
        ################################################################################################################
        class _DummyPU:  # ParallelUtils
            def run_in_parallel(self, fn, fixed, var, n_threads, use_processes):
                out = []  # sequential
                for v in var['variable_dict']:
                    out.append(fn(variable_dict=v, fixed_dict=fixed['fixed_dict'], chain=fixed['chain']))
                return out
        _m.ParallelUtilsClass = _DummyPU
        class _DummyEp:  # EpisodeClass
            def __init__(self, eid=None): self.history = pd.DataFrame()
        _m.EpisodeClass = _DummyEp
        class _DummyChain:  # simple chain
            def generate(self, ep, st):
                ep.history = pd.DataFrame([{'channel': 'assistant', 'agent_id': 'EVAL', 'state_dict': {'score': 1.0}, 'episode_id': st['episode_id'], 'step': 0, 'timestamp': time.time()}])
                return ep, st
        chain = _DummyChain()
        ################################################################################################################
        df = pd.DataFrame({'episode_id': [1, 2]})
        res, hist = DL().run(df=df, chain=chain, fixed_dict={}, max_iter=1, use_wandb=False, n_thread=2)
        print(res.head())

    def test_dataset_generator(self):
        from eigenlib.LLM.dataset_generator import DatasetGeneratorClass
        ################################################################################################################
        ################################################################################################################
        hist = DatasetGeneratorClass().run(source="La Segunda Guerra Mundial", model="gpt-4o", n_questions=2)
        print(hist)

    def test_episode(self):
        from eigenlib.LLM.episode import EpisodeClass
        ################################################################################################################
        ################################################################################################################
        episode = EpisodeClass()
        episode.log(channel='user', modality='text', content='Hola!', agent_id='LLM_0')
        print(episode.history)

    def test_hf_embeddings(self):
        import pandas as pd
        from eigenlib.LLM.hf_embeddings import HFEmbeddingsClass
        ################################################################################################################
        ################################################################################################################
        df = pd.DataFrame({'text': ["El gato está sobre la mesa", "El perro juega en el jardín", "La ciudad de París es hermosa"]})
        h = HFEmbeddingsClass()
        h.initialize()
        df['emb'] = h.fit(df, text_serie='text')
        print(h.get_similarity(df, embeddings_serie='emb', term='¿Dónde está el gato?')[['text', 'score']].head())

    def test_intelligent_web_search(self):
        from eigenlib.LLM.intelligent_web_search import IntelligentWebSearch
        ################################################################################################################
        ################################################################################################################
        source = IntelligentWebSearch().run('F22 Raptor', num_results=1)
        print(source)

    def test_llm_client(self):
        from eigenlib.LLM.llm_client import LLMClientClass
        from eigenlib.LLM.episode import EpisodeClass
        ################################################################################################################
        ################################################################################################################
        episode = EpisodeClass()
        episode.log(channel='user', modality='text', content='Cuenta hasta 10', agent_id='Q')
        answer = LLMClientClass(model='gpt-4.1', temperature=1).run(episode=episode, agent_id='Q')
        print(answer)

    def test_llm_validation_split(self):
        import pandas as pd
        from eigenlib.LLM.llm_validation_split import LLMValidationSplitClass
        ################################################################################################################
        ################################################################################################################
        df = pd.DataFrame({'episode_id': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5], 'text': list('abcdefghij')})
        train_df, test_df = LLMValidationSplitClass().run(df, test_size=0.4, random_seed=0)
        print("train ids:", train_df.episode_id.unique(), "test ids:", test_df.episode_id.unique())

    def test_oai_embeddings(self):
        import pandas as pd
        from eigenlib.LLM.oai_embeddings import OAIEmbeddingsClass
        ################################################################################################################
        ################################################################################################################
        df = pd.DataFrame({'text': ["El gato duerme", "París es la capital de Francia", "Los perros ladran al cartero"]})
        o = OAIEmbeddingsClass()
        o.initialize()
        df['emb'] = o.fit(df, text_serie='text', max_workers=3)
        print(o.get_similarity(df, embeddings_serie='emb', term='¿Dónde está el gato?')[['text', 'score']].head())

    def test_pdf_to_markdown(self):
        import tempfile, os
        from reportlab.pdfgen import canvas
        from eigenlib.LLM.pdf_to_markdown import PDFToMarkdownOCR
        ################################################################################################################
        tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        p = tmp.name
        tmp.close()
        c = canvas.Canvas(p)
        c.setTitle("Prueba")
        c.drawString(100, 750, "TITULO PRINCIPAL")
        c.drawString(100, 720, "Este es un texto de prueba en el PDF.")
        c.save()
        ################################################################################################################
        md = PDFToMarkdownOCR(tesseract_lang='spa').convert_pdf_to_markdown(pdf_path=p)
        print(md)
        os.unlink(p)

    def test_rag_chain(self):
        from eigenlib.LLM.rag_chain import RAGChain
        from eigenlib.LLM.episode import EpisodeClass
        ################################################################################################################
        ################################################################################################################
        chain = RAGChain(agent_model='gpt-4.1', user_model='gpt-4.1', eval_model='gpt-4.1', user_reasoning_effort=None, agent_reasoning_effort=None, eval_reasoning_effort=None, tools_dict={}, tool_choice='none')
        episode = EpisodeClass()
        state_dict = {
            'agent_context': '',
            'agent_instructions': 'Cuenta de 10 a 0.',
            'steering': None,
            'img': None,
            'user_message': '',
        }
        episode, state_dict = chain.predict(episode, state_dict)
        print(state_dict['answer'])

    def test_sources_parser(self):
        import tempfile, os, pandas as pd
        from reportlab.pdfgen import canvas
        from eigenlib.LLM.sources_parser import SourcesParserClass
        ################################################################################################################
        pdf_tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        pdf_path = pdf_tmp.name
        pdf_tmp.close()
        c = canvas.Canvas(pdf_path)
        c.drawString(100, 750, "Contenido PDF de prueba")
        c.save()
        ################################################################################################################
        sp = SourcesParserClass()
        pdf_text = sp.run(file_path=pdf_path, lang='spa', mode='pdf')
        url_text = sp.run(file_path='https://example.com', lang='spa')
        df_batch = sp.run_batch(raw_sources=[pdf_path, 'https://example.com'], lang='spa')
        print(pdf_text[:100], url_text[:100], df_batch.head())
        os.unlink(pdf_path)

    def test_vector_database(self):
        from eigenlib.LLM.vector_database import VectorDatabaseClass
        import requests
        ################################################################################################################
        ################################################################################################################
        source = requests.get("https://es.wikipedia.org/wiki/Título_de_la_página").text
        VDB = VectorDatabaseClass()
        VDB.initialize()
        source_df = VDB.create(source[0:300], separator='.', create_vectors=True, chunking_threshold=200)
        print(source_df)

    def test_web_parser(self):
        from eigenlib.LLM.web_parser import WebParserClass
        ################################################################################################################
        ################################################################################################################
        parser = WebParserClass("https://es.wikipedia.org/wiki/Lockheed_Martin_F-22_Raptor")
        content = parser.run()
        print(content)

class UnitTestMLClass(unittest.TestCase):
    def setUp(self):
        from eigenlib.utils.testing_utils import TestingUtilsClass, module_test_coverage
        ################################################################################################################
        module_test_coverage('eigenlib.ML', self)
        self.test_df, self.model, self.image, self.texto = TestingUtilsClass().get_dummy_data()

    def test_basic_model_loader(self):
        import tempfile, os, sys, types
        class _DummyDB:
            def __init__(self, *_, **__): pass

            def cloud_upload_file(self, *_, **__): pass

            def cloud_download_file(self, *_, **__): pass

        import eigenlib.ML.basic_model_loader as _bml
        _bml.DatabricksStorageUtilsClass = _DummyDB
        # ---- env vars ---------------------------------------------------------------
        tmp = tempfile.mkdtemp()
        os.environ['MODELS_PATH'] = tmp
        os.environ['CURATED_DATA_PATH'] = tmp
        os.environ['CLOUD_ROOT'] = tmp
        os.environ['DATABRICKS_INSTANCE'] = 'dummy'
        os.environ['DB_TOKEN'] = 'dummy'
        # ---- test -------------------------------------------------------------------
        from eigenlib.ML.basic_model_loader import BasicModelLoaderClass
        mdl = BasicModelLoaderClass(cloud=True, save_model=True)
        mdl.save('test_model', {'hello': 'world'})
        print(mdl.load('test_model'))
        os.unlink(os.path.join(tmp, 'test_model.pkl'))
        os.rmdir(tmp)

    def test_basic_validation_split(self):
        import pandas as pd
        from eigenlib.ML.basic_validation_split import BasicValidationSplitClass
        X = pd.DataFrame({'f1': range(10), 'f2': range(10, 20)})
        y = pd.Series([0, 1] * 5)
        bvs = BasicValidationSplitClass(split_seed=42, train_size=0.7, val_size=0.15, test_size=0.15, split_feature=None)
        X_tr, y_tr, X_val, y_val, X_te, y_te, _ = bvs.transform(X, y)
        print(len(X_tr), len(X_val), len(X_te))

    def test_catboost_model(self):
        import pandas as pd
        from eigenlib.ML.catboost_model import ModelCatboostClass
        ################################################################################################################
        X = pd.DataFrame({'a': range(8), 'b': range(8, 16)})
        y = pd.DataFrame({'target': [0, 1, 0, 1, 0, 1, 0, 1]})
        X_tr, y_tr = X.iloc[:4], y.iloc[:4]
        X_val, y_val = X.iloc[4:6], y.iloc[4:6]
        X_te, y_te = X.iloc[6:], y.iloc[6:]
        ################################################################################################################
        mc = ModelCatboostClass(params_dict={'iterations': 20, 'depth': 2, 'verbose': False}, problem_mode='classification', use_calibration=False)
        mc.initialize(X_tr, y_tr)
        mc.fit(X_tr, y_tr, X_val, y_val, X_te, y_te)
        _, preds, _ = mc.predict(X_te)
        print(preds)

    def test_custom_transform(self):
        import pandas as pd
        from eigenlib.ML.custom_transform import CustomTransformClass
        ################################################################################################################
        X = pd.DataFrame({'a': [1, 2, 3]})
        y = pd.Series([0, 1, 0])
        ################################################################################################################
        ct = CustomTransformClass()
        ct.fit(X, y)
        X_t, y_t, _ = ct.transform(X, y)
        print(X_t, y_t.tolist())

    def test_ensemble_model(self):
        import numpy as np, pandas as pd
        from eigenlib.ML.ensemble_model import BlendingEnsemble
        ################################################################################################################
        ################################################################################################################
        class _DummyBase:  # mock model for base level
            def initialize(self, *a, **k): pass

            def fit(self, *a, **k): pass

            def predict(self, X, metadata=None):
                return None, pd.DataFrame({'pred': np.zeros(len(X))}), metadata
        class _DummyMeta:  # mock model for meta level
            def initialize(self, *a, **k): pass

            def fit(self, *a, **k): pass

            def predict(self, X):
                return pd.DataFrame({'final_pred': np.zeros(len(X))})
        X = pd.DataFrame({'f1': range(10), 'f2': range(10, 20)})
        y = pd.DataFrame({'target': [0, 1] * 5})

        ens = BlendingEnsemble(base_models=[_DummyBase(), _DummyBase()], meta_model=_DummyMeta(), problem_mode='classification', test_size_meta=0.2, random_state=42)
        ens.initialize()
        ens.fit(X, y, X, y, X, y, {})
        print(ens.predict(X).head())

    def test_etl_dummy(self):
        import tempfile, os, shutil
        from eigenlib.ML.etl_dummy import ETLDummyClass
        import eigenlib.utils.data_utils as du
        ################################################################################################################
        ################################################################################################################
        du.DataUtilsClass.save_dataset = lambda *a, **k: None
        tmp = tempfile.mkdtemp()
        os.environ['CURATED_DATA_PATH'] = tmp
        X, y, _ = ETLDummyClass(dataset_name='dummy_dataset', n_shards=1, cloud=False).run()
        print(X.head())
        shutil.rmtree(tmp)

    def test_feature_category_encoder(self):
        import pandas as pd
        from eigenlib.ML.feature_category_encoder import FeatureCategoryEncoderClass
        ################################################################################################################
        X = pd.DataFrame({'color': ['rojo', 'azul', 'rojo', 'verde'], 'valor': [1, 2, 3, 4]})
        y = pd.Series([0, 1, 0, 1])
        ################################################################################################################
        fce = FeatureCategoryEncoderClass(encoding_type='TargetEncoder', encoding_features=['color'])
        fce.fit(X, y)
        X_enc, _, _ = fce.transform(X, y)
        print(X_enc.head())

    def test_feature_scaling(self):
        import pandas as pd
        from eigenlib.ML.feature_scaling import FeatureScalingClass
        ################################################################################################################
        X = pd.DataFrame({'num1': [1, 2, 3, 4], 'num2': [10, 20, 30, 40]})
        y = pd.Series([0, 1, 0, 1])
        ################################################################################################################
        fs = FeatureScalingClass(scaling_type='StandardScaler', scaling_features=['num1', 'num2'])
        fs.fit(X, y)
        X_scaled, _, _ = fs.transform(X.copy(), y)
        X_restored, _, _ = fs.inverse_transform(X_scaled.copy(), y)
        print(X_scaled.head(), X_restored.head())

    def test_feature_selection(self):
        import pandas as pd
        from eigenlib.ML.feature_selection import FeatureSelectionClass
        ################################################################################################################
        X = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]})
        y = pd.Series([0, 1, 0])
        ################################################################################################################
        fs = FeatureSelectionClass(selected_features=['a', 'c'])
        fs.fit(X, y)
        X_sel, _, _ = fs.transform(X, y)
        print(X_sel)

    def test_general_ml_experiment(self):
        import pandas as pd
        from eigenlib.ML.general_ml_experiment import GeneralMLExperiment
        ################################################################################################################
        class _MockExp:
            def run(self): return pd.DataFrame({'accuracy': [0.85]})
        class _MockLogger:
            def run(self, df): print("logged:", df['accuracy'].iloc[0])

        ################################################################################################################
        GeneralMLExperiment(exp_module=_MockExp(), search_metric='accuracy', use_logger=True, logger_module=_MockLogger(), hparam_tuning=False).run()

    @unittest.skip("TODO")
    def test_general_ml_pipeline(self):
        import tempfile, os, pandas as pd, numpy as np
        from eigenlib.ML.general_ml_pipeline import GeneralMLPipelineClass
        import eigenlib.utils.data_utils as du
        tmp = tempfile.mkdtemp()
        os.environ['CURATED_DATA_PATH'] = tmp
        os.environ['RAW_DATA_PATH'] = tmp + os.sep
        def _fake_loader(*_, **__):
            return pd.DataFrame({'f1': [1, 2, 3, 4], 'f2': [0, 1, 0, 1], 'target': [0, 1, 0, 1]})
        du.DataUtilsClass.load_dataset = lambda self, *a, **k: _fake_loader()

        # --- mocks ------------------------------------------------------------------
        class _DummyETL:
            def run(self, *_):
                df = pd.DataFrame({'f1': [1, 2, 3, 4], 'f2': [0, 1, 0, 1], 'target': [0, 1, 0, 1]})
                return df.drop(columns=['target']), df[['target']], {}

        class _SPP1:
            def transform(self, df, _, meta):
                y = df[['target']];
                X = df.drop(columns=['target'])
                return X, y, meta

        class _Passthrough:
            def fit(self, *_): pass

            def transform(self, X, y, m): return X, y, m

        class _DummyModel:
            def initialize(self, *_): pass

            def fit(self, *_): pass

            def predict(self, X, *_):
                return None, pd.DataFrame({'predictions': np.zeros(len(X))}, index=X.index), {}

        class _DummyMetrics:
            def run(self, y_true, y_pred, meta):
                return pd.DataFrame({'dummy_metric': [1.0]}), meta

        class _DummyLogger:
            def run(self, df): print("logger metric:", df.iloc[0, 0])

        class _DummyLoader:
            def save(self, *_): pass

            # --- pipeline instantiation -------------------------------------------------
        data_cfg = {'dataset_name': 'dummy', 'hparams_grid': {}, 'model_id': 'test_pipeline', 'checkpoint': 3}
        pl = GeneralMLPipelineClass(data_cfg, ETL=_DummyETL(), spp_1=_SPP1(), spp_2=_Passthrough(), spp_3=_Passthrough(), val_split=_Passthrough(), dpp_1=_Passthrough(), dpp_2=_Passthrough(), dpp_3=_Passthrough(), dpp_4=_Passthrough(), model=_DummyModel(), pos_1=_Passthrough(), pos_2=_Passthrough(), metrics=_DummyMetrics(), logger=_DummyLogger(), model_loader=_DummyLoader())

        print(pl.train())
        os.rmdir(tmp)
        pass

    def test_identity(self):
        import pandas as pd
        from eigenlib.ML.identity import IdentityClass
        ################################################################################################################
        X = pd.DataFrame({'a': [1, 2, 3]})
        y = pd.Series([0, 1, 0])
        ################################################################################################################
        iden = IdentityClass()
        iden.fit(X, y)
        X_t, y_t, _ = iden.transform(X, y)
        print(X_t.equals(X), y_t.tolist())

    def test_imputer(self):
        import pandas as pd, numpy as np
        from eigenlib.ML.imputer import ImputerClass
        ################################################################################################################
        df = pd.DataFrame({'num': [1, np.nan, 3], 'cat': ['x', np.nan, 'y']})
        ################################################################################################################
        imp = ImputerClass()
        imp.fit(df)
        df_filled, _, _ = imp.transform(df)
        print(df_filled)

    def test_lgbm_model(self):
        import pandas as pd
        from sklearn.datasets import load_iris
        from eigenlib.ML.lgbm_model import LGBMModelClass
        ################################################################################################################
        d = load_iris()
        X = pd.DataFrame(d.data)
        y = pd.DataFrame(d.target, columns=['t'])
        X_tr, y_tr = X.iloc[:120], y.iloc[:120]  # contiene 0,1,2
        X_val, y_val = X.iloc[120:135], y.iloc[120:135]
        X_te, y_te = X.iloc[135:], y.iloc[135:]
        ################################################################################################################
        model = LGBMModelClass(params_dict={'n_estimators': 30, 'learning_rate': 0.1, 'verbose': -1}, categories=[0, 1, 2], use_calibration=False)
        model.initialize()
        model.fit(X_tr, y_tr, X_val, y_val, X_te, y_te)
        _, preds, _ = model.predict(X_te)
        print(preds.head())

    def test_metrics_classification_regression(self):
        import pandas as pd
        from eigenlib.ML.metrics_classification_regression import MetricsClassificationRegressionClass
        ################################################################################################################
        ################################################################################################################
        m = MetricsClassificationRegressionClass(mode='classification')
        df, _ = m.run(pd.Series([0, 1, 1, 0]), pd.Series([0, 1, 0, 0]))
        print(df)

    def test_pytorch_nn_model(self):
        import numpy as np, pandas as pd
        from eigenlib.ML.pytorch_nn_model import PytorchNNModelClass
        ################################################################################################################
        X = pd.DataFrame(np.random.rand(20, 9))
        y = pd.DataFrame({'label': np.random.randint(0, 2, 20)})
        X_tr, y_tr = X.iloc[:12], y.iloc[:12]  # train
        X_val, y_val = X.iloc[12:16], y.iloc[12:16]  # val
        X_te, y_te = X.iloc[16:], y.iloc[16:]  # test
        ################################################################################################################
        nn = PytorchNNModelClass(learning_rate=0.01, batch_size=4, epochs=3, early_stopping_patience=2, hidden_size=5, dropout_rate=0.1, device='cpu', print_every=100)
        nn.fit(X_tr, y_tr, X_val, y_val, X_te, y_te)
        _, preds, _ = nn.predict(X_te)
        print(preds.head())

    def test_shallow_models(self):
        import pandas as pd, numpy as np
        from eigenlib.ML.shallow_models import Shallow_Models
        ################################################################################################################
        X = pd.DataFrame({'f1': np.random.rand(20), 'f2': np.random.rand(20)})
        y = pd.DataFrame({'target': np.random.randint(0, 2, 20)})
        X_tr, y_tr = X.iloc[:10], y.iloc[:10]
        X_val, y_val = X.iloc[10:15], y.iloc[10:15]
        X_te, y_te = X.iloc[15:], y.iloc[15:]
        ################################################################################################################
        m = Shallow_Models(params_dict={'n_estimators': 10}, model_type='RandomForest', problem_mode='classification', prediction_mode='predict')
        m.initialize()
        m.fit(X_tr, y_tr, X_val, y_val, X_te, y_te)
        _, p, _ = m.predict(X_te)
        print(p.head())

    def test_target_feature(self):
        import pandas as pd
        from eigenlib.ML.target_feature import TargetFeatureClass
        ################################################################################################################
        df = pd.DataFrame({'a': [1, 2, 3], 'target': [0, 1, 0]})
        ################################################################################################################
        tf = TargetFeatureClass(target_features=['target'])
        X, y, _ = tf.transform(df, None, {})
        print(X, y)

    def test_wandb_logging(self):
        from eigenlib.ML.wandb_logging import WandbLoggingClass
        ################################################################################################################
        class _DummyRun:
            def log(self, d): print("wandb.log:", d)

            def finish(self): print("wandb.finish")

        class _DummyWandb:
            def init(self, project=None, name=None):
                print(f"wandb.init(project={project}, name={name})")
                return _DummyRun()

            def finish(self): print("wandb.finish")
        ################################################################################################################
        import eigenlib.ML.wandb_logging as wl
        wl.wandb = _DummyWandb()  # monkey-patch
        w = WandbLoggingClass(run_name='test_run', project_name='test_proj', logging=True)
        w.initialice()
        w.run(score_dict={'accuracy': 0.92, 'loss': 0.1})
        w.end_run()

    def test_xgb_model(self):
        import numpy as np, pandas as pd
        from eigenlib.ML.xgb_model import ModelXGBClass
        # datos dummy (30 filas, 4 features numéricos) -------------------------------
        X = pd.DataFrame(np.random.rand(30, 4))
        y = pd.DataFrame({'label': np.random.randint(0, 2, 30)})
        X_tr, y_tr = X.iloc[:20], y.iloc[:20]  # train
        X_val, y_val = X.iloc[20:25], y.iloc[20:25]  # val
        X_te, y_te = X.iloc[25:], y.iloc[25:]  # test
        # parámetros mínimos para XGBoost -------------------------------------------
        params = {'objective': 'binary:logistic', 'eval_metric': 'logloss', 'num_boost_round': 20, 'early_stopping_rounds': 5, 'verbosity': 0}
        # test ----------------------------------------------------------------------
        xgbm = ModelXGBClass(params_dict=params, problem_mode='classification', use_calibration=False)
        xgbm.initialize()
        xgbm.fit(X_tr, y_tr, X_val, y_val, X_te, y_te)
        _, preds, _ = xgbm.predict(X_te)
        print(preds.head())

class UnitTestUtilsClass(unittest.TestCase):

    def setUp(self):
        from eigenlib.utils.testing_utils import TestingUtilsClass, module_test_coverage
        ################################################################################################################
        module_test_coverage('eigenlib.utils', self)
        self.test_df, self.model, self.image, self.texto = TestingUtilsClass().get_dummy_data()

    def test_alert_utils(self):
        import os
        from eigenlib.utils.alert_utils import alerts
        ################################################################################################################
        alerts('test_message', bot_token=os.environ.get('TELEGRAM_BOT_TOKEN_2'), bot_chatID=int(os.environ.get('TELEGRAM_CHAT_ID_2')))

    def test_data_utils(self):
        from eigenlib.utils.data_utils import DataUtilsClass
        import os
        ################################################################################################################
        ################################################################################################################
        DataUtilsClass.save_dataset(self.test_df, path=os.environ['CURATED_DATA_PATH'], dataset_name='test_dataset', format='parquet', n_threads=8, cloud=False)
        df = DataUtilsClass.load_dataset(path=os.environ['CURATED_DATA_PATH'], dataset_name='test_dataset', format='parquet')
        DataUtilsClass.save_dataframe(self.test_df, path=os.environ['CURATED_DATA_PATH'], filename='test_file', format='parquet')
        df = DataUtilsClass.load_dataframe(path=os.environ['CURATED_DATA_PATH'], filename='test_file', format='parquet')
        folder_path = os.path.join(os.environ['RAW_DATA_PATH'], 'test_parquet')
        DataUtilsClass.compress(folder_path, folder_path + '.zip')
        folder_path = os.path.join(os.environ['RAW_DATA_PATH'], 'test_parquet')
        DataUtilsClass.decompress(folder_path + '.zip', folder_path)
        os.remove(os.path.join(folder_path + '.zip'))

    @unittest.skip("Test manual")
    def test_databricks_serving_utils(self):
        from eigenlib.utils.databricks_serving_utils import DatabricksEndpointServingClass, DatabricksJobLaunchClass
        ################################################################################################################
        ################################################################################################################
        code = """print('Hola mundo')"""
        cluster = ['0512-135345-xrtfjvg1'][0]
        job_name = 'test_job'
        DatabricksJobLaunchClass().run_job_from_code(code, cluster, job_name)
        class TestDeploymentClass:
            def __init__(self):
                pass

            def run(self, config):
                config['answer'] = eval(config['code'])
                return config
        config = {}
        DBES = DatabricksEndpointServingClass(endpoint_name="test_endpoint", MainClass=TestDeploymentClass, api_root=None, api_token=None)
        DBES.deploy(config)

    def test_databricks_storage_utils(self):
        import os
        from eigenlib.utils.databricks_storage_utils import DatabricksStorageUtilsClass
        ################################################################################################################
        file_name = 'test_dataset.pkl'
        self.test_df.to_pickle(os.path.join(os.environ['CURATED_DATA_PATH'], file_name))
        client = DatabricksStorageUtilsClass(DATABRICKS_INSTANCE=os.environ['DATABRICKS_INSTANCE'], TOKEN=os.environ['DB_TOKEN'])
        client.cloud_upload_file(os.environ['CURATED_DATA_PATH'], os.path.join(os.environ['CLOUD_ROOT'], os.environ['CURATED_DATA_PATH']), file_name)
        os.remove(os.path.join(os.environ['CURATED_DATA_PATH'], file_name))
        client.cloud_download_file(os.environ['CURATED_DATA_PATH'], os.path.join(os.environ['CLOUD_ROOT'], os.environ['CURATED_DATA_PATH']), file_name)
        os.remove(os.path.join(os.environ['CURATED_DATA_PATH'], file_name))
        client.cloud_delete(os.path.join(os.environ['CLOUD_ROOT'], os.environ['CURATED_DATA_PATH']), file_name)

    def test_encryption_utils(self):
        import os
        from eigenlib.utils.encryption_utils import EncryptionUtilsClass
        ################################################################################################################
        ################################################################################################################
        EU = EncryptionUtilsClass()
        public_key = EU.initialize()
        encrypted_password = EU.encrypt_pass('Hola mundo', public_key)
        password = EU.decrypt_pass(encrypted_password)
        file = os.path.join(os.environ['RAW_DATA_PATH'], 'test_image', 'test_file.jpg')
        EU.encrypt_file(file, file + '.enc', password=password)
        EU.decrypt_file(file + '.enc', file, password=password)

    def test_img_utils(self):
        import os
        import shutil
        from eigenlib.utils.img_utils import ImageUtilsClass
        import pandas as pd
        import tempfile
        from PIL import Image
        ################################################################################################################
        test_url = "https://httpbin.org/image/jpeg"  # URL de prueba que devuelve una imagen
        temp_dir = tempfile.mkdtemp()
        try:
            ImageUtilsClass.download_img(url=test_url, path=temp_dir, filename="test_image.jpg", jpeg_quality=60)
            downloaded_file = os.path.join(temp_dir, "test_image.jpg")
            self.assertTrue(os.path.exists(downloaded_file))
            data_url = ImageUtilsClass.local_image_to_data_url(downloaded_file)
            self.assertTrue(data_url.startswith("data:image/png;base64,"))
            self.assertTrue(len(data_url) > 50)  # Verificar que contiene datos
        finally:
            shutil.rmtree(temp_dir)
        test_df = pd.DataFrame({'image_url': [
                "https://httpbin.org/image/jpeg",
                "https://httpbin.org/image/png"
            ], 'image_name': ['test_img_1', 'test_img_2']})
        temp_dir = tempfile.mkdtemp()
        try:
            ImageUtilsClass.download_img_dataset(df=test_df, path=temp_dir, url_serie='image_url', name_serie='image_name', dataset_name='test_dataset', n_shards=2)
            dataset_path = os.path.join(temp_dir, 'image_name')
            self.assertTrue(os.path.exists(dataset_path))
            img1_path = os.path.join(dataset_path, 'test_img_1.jpg')
            img2_path = os.path.join(dataset_path, 'test_img_2.jpg')
            print(f"Imagen 1 descargada: {os.path.exists(img1_path)}")
            print(f"Imagen 2 descargada: {os.path.exists(img2_path)}")
        finally:
            shutil.rmtree(temp_dir)
        temp_dir = tempfile.mkdtemp()
        try:
            test_image = Image.new('RGB', (100, 100), color='red')
            test_image_path = os.path.join(temp_dir, 'test_created_image.png')
            test_image.save(test_image_path)
            data_url = ImageUtilsClass.local_image_to_data_url(test_image_path)
            self.assertTrue(data_url.startswith("data:image/png;base64,"))
            self.assertTrue(len(data_url) > 100)
        finally:
            shutil.rmtree(temp_dir)
        print("Todos los tests de ImageUtilsClass completados exitosamente")

    def test_nano_net(self):
        from eigenlib.utils.nano_net import NanoNetClass
        ################################################################################################################
        master = NanoNetClass()
        master.launch_master()
        ################################################################################################################
        node_A = NanoNetClass()
        def node_A_method(a, b):
            return a + b
        node_A.launch_node(node_name='node_A', node_method=node_A_method, master_address='tcp://localhost:5000', password='test_password', delay=1)
        ################################################################################################################
        node_B = NanoNetClass()
        node_B.launch_node(node_name='node_B', node_method=None, master_address='tcp://localhost:5000', password='test_password', delay=1)
        out = node_B.call(address_node='node_A', payload={'a': 1, 'b': 2})
        print(out)
        master.stop()
        node_A.stop()
        node_B.stop()

    def test_nano_server(self):
        from eigenlib.utils.nano_server import NanoServerClass
        import pandas as pd
        ################################################################################################################
        password = 'test_pass'
        ################################################################################################################
        server = NanoServerClass()
        def aux_method(input_of_method=None):
            return pd.DataFrame([input_of_method])
        server.launch_server(aux_method, address='tcp://*:5005', password=password)
        client = NanoServerClass()
        result = client.call({'input_of_method': 1}, address='tcp://localhost:5005', password=password)
        client.stop()
        server.stop()
        print(result)

    def test_notion_utils(self):
        from eigenlib.utils.notion_utils import NotionUtilsClass
        ################################################################################################################
        NU = NotionUtilsClass()
        NU.write(page_id='2432a599e985804692b7d6982895a2b2', texto='* ' + 'This is a test.')

    def test_parallel_utils(self):
        from eigenlib.utils.parallel_utils import ParallelUtilsClass
        def test_function(a, b, c=1):
            return a + b + c
        fixed_args = {'c': 10}
        variable_args = {
            'a': [1, 2, 3, 4],
            'b': [10, 20, 30, 40]
        }
        results = ParallelUtilsClass.run_in_parallel(aux_function=test_function, fixed_args=fixed_args, variable_args=variable_args, n_threads=4, use_processes=False)
        print(results)

    def test_project_setup(self):
        from eigenlib.utils.project_setup import ProjectSetupClass
        ################################################################################################################
        ################################################################################################################
        ProjectSetupClass(project_folder='swarm-automations', test_environ=True)

    @unittest.skip("Test needs vpn")
    def test_snowflake_utils(self):
        from eigenlib.utils.snowflake_utils import SnowflakeUtilsClass
        ################################################################################################################
        ################################################################################################################
        client = SnowflakeUtilsClass()
        table_path = "ANALYTICS.PURCHASE.ESCANDALLOS"
        result = client.query(f"SELECT * FROM {table_path}")
        print(result)

    def test_system_monitor(self):
        import asyncio, threading
        from eigenlib.utils.system_monitor import AsyncSystemMonitor
        ################################################################################################################
        ################################################################################################################
        def runner():
            mon = AsyncSystemMonitor()
            async def main(): await mon.start(); await asyncio.sleep(3); await mon.stop()
            asyncio.run(main())
        threading.Thread(target=runner, daemon=True).start()

    def test_telegram_utils(self):
        from eigenlib.utils.telegram_utils import TelegramUtilsClass
        import time
        def mi_callback(input_message):
            print(f"📩 Nuevo mensaje: {input_message}")
        tg = TelegramUtilsClass('8274428979:AAESesYIWiCkwiGJynEokgFmrqKKhwemI3Q', -1002504088542)
        tg.listen(mi_callback)
        time.sleep(2)
        tg.send_message("¡Hola a todos!", sender="MiBot")
        time.sleep(2)
        tg.stop()

    def test_testing_utils(self):
        import os
        from eigenlib.utils.testing_utils import TestingUtilsClass
        from PIL import Image
        from fpdf import FPDF
        ################################################################################################################
        ################################################################################################################
        df, model, image, texto = TestingUtilsClass().get_dummy_data()
        # Crear carpetas de salida
        os.makedirs(os.path.join(os.environ['RAW_DATA_PATH'],"test_pdf"), exist_ok=True)
        os.makedirs(os.path.join(os.environ['RAW_DATA_PATH'],"test_excel"), exist_ok=True)
        os.makedirs(os.path.join(os.environ['RAW_DATA_PATH'],"test_parquet"), exist_ok=True)
        os.makedirs(os.path.join(os.environ['RAW_DATA_PATH'],"test_image"), exist_ok=True)
        os.makedirs(os.path.join(os.environ['RAW_DATA_PATH'],"test_text"), exist_ok=True)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in texto.split("\n"):
            pdf.multi_cell(0, 10, line)
        pdf.output(os.path.join(os.environ['RAW_DATA_PATH'], "test_pdf/test_file.pdf"))

        # 2. Guardar DataFrame como Excel
        df.to_excel(os.path.join(os.environ['RAW_DATA_PATH'],"test_excel/test_file.xlsx"), index=False)

        # 3. Guardar DataFrame como Parquet
        df.to_parquet(os.path.join(os.environ['RAW_DATA_PATH'],"test_parquet/test_file.parquet"), index=False)

        # 4. Guardar imagen como JPG
        if isinstance(image, Image.Image):  # Asegurarse de que es un objeto PIL.Image
            image.convert("RGB").save(os.path.join(os.environ['RAW_DATA_PATH'],"test_image/test_file.jpg"), "JPEG")
        else:
            raise TypeError("La imagen no es un objeto PIL.Image")

        # 5. Guardar texto como .txt
        with open(os.path.join(os.environ['RAW_DATA_PATH'],"test_text/test_file.txt"), "w", encoding="utf-8") as f:
            f.write(texto)

        TestingUtilsClass().checkpoint(df)
        test_dict = TestingUtilsClass().get()

    def test_youtube_utils(self):
        import tempfile, os
        from eigenlib.utils.youtube_utils import YoutubeUtilsClass
        ################################################################################################################
        out_dir = tempfile.mkdtemp()
        ################################################################################################################
        yt = YoutubeUtilsClass(quiet=True, no_warnings=True)
        file_path = yt.download_audio(video_url='https://www.youtube.com/watch?v=E9de-cmycx8', output_dir=out_dir, filename='test_audio', compress=False)
        print(f"size MB: {yt.get_file_size_mb(file_path):.2f}")
        os.unlink(file_path)
        os.rmdir(out_dir)

if __name__ == '__main__':
    unittest.main()
