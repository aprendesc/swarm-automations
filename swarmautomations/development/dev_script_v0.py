from eigenlib.utils.project_setup import ProjectSetupClass
ProjectSetupClass(project_folder='swarm-automations')

import sys
import pytest

def main():
    pytest_args = ["tests/", "--cov=my_package", "--cov-report=term-missing"]
    exit_code = pytest.main(pytest_args)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()


if False:
    # swarmautomations
    ## Main scripts
    from swarmautomations.main import MainClass
    from swarmautomations.config import test_config
    ### Modules
    from swarmautomations.modules.automatic_summarizer import SourceSummarizationClass
    from swarmautomations.modules.call_recording_pipeline import CallRecordingPipelineClass
    from swarmautomations.modules.standby import StandbyClass
    # eigenlib
    ## Audio
    from eigenlib.audio.audio_utils import AudioUtilsClass
    from eigenlib.audio.oai_whisper_stt import OAIWhisperSTTClass
    from eigenlib.audio.light_speech_recognition import LightSpeechRecognitionClass
    from eigenlib.audio.audio_mixer_recorder import AudioMixerRecorder
    from eigenlib.audio.OAI_TTS import OAITTSModelClass
    from eigenlib.audio.keyword_trigger import KeywordTriggerClass
    ## Image
    from eigenlib.image.CLIP_embedding_model import ClipEmbeddingsModel
    from eigenlib.image.dalle_model import DalleModelClass
    ## LLM
    from eigenlib.LLM.web_parser import WebParserClass
    from eigenlib.LLM.llm_client import LLMClientClass
    from eigenlib.LLM.episode import EpisodeClass
    from eigenlib.LLM.dataset_generator import DatasetGeneratorClass
    from eigenlib.LLM.oai_embeddings import OAIEmbeddingsClass
    from eigenlib.LLM.intelligent_web_search import IntelligentWebSearch
    from eigenlib.LLM.computer_use_tools import ComputerUseClass
    from eigenlib.LLM.vector_database import VectorDatabaseClass
    from eigenlib.LLM.rag_chain import RAGChain
    from eigenlib.LLM.llm_validation_split import LLMValidationSplitClass
    from eigenlib.LLM.base_agent_tools import VDBToolClass
    from eigenlib.LLM.pdf_to_markdown import PDFToMarkdownOCR
    from eigenlib.LLM.hf_embeddings import HFEmbeddingsClass
    from eigenlib.LLM.dataset_autolabeling import DatasetAutolabelingClass
    ## LLM
    from eigenlib.ML.pytorn_nn_model import NN_pytorch_Model
    from eigenlib.ML.xgb_model import ModelXGBClass
    from eigenlib.ML.lgbm_model import LGBMModelClass
    from eigenlib.ML.catboost_model import ModelCatboostClass
    from eigenlib.ML.general_ml_experiment import GeneralMLExperiment
    from eigenlib.ML.general_ml_pipeline import GeneralMLPipelineClass
    from eigenlib.ML.ensemble_model import BlendingEnsemble
    from eigenlib.ML.target_feature import TargetFeatureClass
    from eigenlib.ML.basic_model_loader import BasicModelLoaderClass
    from eigenlib.ML.metrics_classification_regression import MetricsClassificationRegressionClass
    from eigenlib.ML.feature_scaling import FeatureScalingClass
    from eigenlib.ML.etl_dummy import ETLDummyClass
    from eigenlib.ML.time_series_validation_split import ValidationSplitTimeSeriesClass
    from eigenlib.ML.imputer import ImputerClass
    from eigenlib.ML.identity import IdentityClass
    from eigenlib.ML.wandb_logging import WandbLoggingClass
    ## Utils
    from eigenlib.utils.alert_utils import alerts
    from eigenlib.utils.api_utils import fastAPIClass
    from eigenlib.utils.data_utils import DataUtilsClass
    from eigenlib.utils.databricks_serving_utils import DatabricksEndpointServingClass
    from eigenlib.utils.databricks_storage_utils import DatabricksStorageUtilsClass
    from eigenlib.utils.encryption_utils import EncryptionUtilsClass
    from eigenlib.utils.img_utils import ImageUtilsClass
    from eigenlib.utils.nano_net import NanoNetClass
    from eigenlib.utils.nano_server import NanoServerClass
    from eigenlib.utils.notion_utils import NotionUtilsClass
    from eigenlib.utils.parallel_utils import ParallelUtilsClass
    from eigenlib.utils.project_setup import ProjectSetupClass
    from eigenlib.utils.snowflake_utils import SnowflakeUtilsClass
    from eigenlib.utils.system_monitor import AsyncSystemMonitor
    from eigenlib.utils.tcp_utils import TCPServerClass
    from eigenlib.utils.telegram_utils import TelegramUtilsClass
    from eigenlib.utils.testing_utils import TestingUtilsClass
    from eigenlib.utils.youtube_utils import YoutubeUtilsClass
