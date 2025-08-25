from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from eigenlib.LLM.sources_parser import SourcesParserClass
from eigenlib.LLM.episode import EpisodeClass
from eigenlib.LLM.llm_client import LLMClientClass
from eigenlib.audio.oai_tts import OAITTSModelClass
from eigenlib.image.dalle_model import DalleModelClass
import os
import pandas as pd
import numpy as np
import soundfile as sf
import time

class PodcastGeneration:
    def __init__(self):
        pass

    def run(self, max_iter, podcast_path):
        SP = SourcesParserClass()
        path = 'C:/Users/AlejandroPrendesCabo/Desktop/proyectos/swarm-automations/data/raw/source_papers'
        ########################################################################################################################
        files = os.listdir(path)
        print(pd.Series(files))
        selection = int(input('Seleccione el paper a generar: '))
        max_iter = int(input('Introduce max iter: '))
        input_file = os.path.join(path, files[selection])
        path = input_file
        name = input_file.replace('.pdf', '').split('\\')[-1]

        source = SP.run(path)
        podcast_path = os.path.join(podcast_path, name)
        os.makedirs(podcast_path, exist_ok=True)
        Q_system_prompt = f"""Fuente de información que debes emplear:\n'{source}
Eres un entrevistador del podcast Aligned Humans llamado Light y tu objetivo es ir manteniendo un dialogo. Realiza preguntas cortas en orden, inteligentes, avanzadas, con mucho sentido haciendo al entrevistado sentirse cómodo.
El podcast constará en total de {str(max_iter)} preguntas, así que estructura tus preguntas de forma adecuada para cubrir con ese nivel de detalle asumiento que el oyente ya tiene un alto conocimiento de IA.
"""
        A_system_prompt = f"""Fuente de información que debes emplear para responder en el podcast: \n'{source}
Eres Signal una experta que esta realizando un podcast y tu objetivo es ir manteniendo una conversación técnica pero muy amena sobre las preguntas que el entrevistador llamado (Light) te va a ir haciendo usando el conocimiento de la fuente. Tus respuestas deben ser breves y dinámicas pero cargadas de contenido y de insight, sin miedo a sonar técnica. Asume que oyente ya tiene conocimientos avanzados de IA. Recuerda ser breve y al grano.
    """

        episode = EpisodeClass()
        episode.log(channel='system', modality='text', content=Q_system_prompt, agent_id='Q')
        episode.log(channel='system', modality='text', content=A_system_prompt, agent_id='A')

        A_message = """Genera una introducción al podcast, por ejemplo 'Bienvenidos a aligned humans, el espacio de donde sincronizamos al humano con la realidad de la inteligencia artificial. Prepara tus conexiones neuronales porque comienza el viaje. Hoy tenemos con nosotros a... (presentación breve de la invitada llamada Signal experta en la fuente que es quien entrevistarás, presentala un poco.)'"""
        for i in range(0, max_iter):
            print(i)
            start_time = time.time()

            episode.log(channel='system', modality='text', content=f'Haz la pregunta número {str(i)}', agent_id='Q')
            episode.log(channel='user', modality='text', content=A_message, agent_id='Q')
            Q_message = LLMClientClass(model='gpt-4.1', temperature=1).run(episode, agent_id='Q')
            episode.log(channel='assistant', modality='text', content=Q_message, agent_id='Q')

            OAITTSModelClass(voice='echo').run(Q_message.encode('utf-8').decode('utf-8'), podcast_path + f'/turno_{str(i)}_int.mp3')

            episode.log(channel='user', modality='text', content=Q_message, agent_id='A')
            A_message = LLMClientClass(model='gpt-4.1', temperature=1).run(episode, agent_id='A')
            episode.log(channel='assistant', modality='text', content=A_message, agent_id='A')
            OAITTSModelClass(voice='nova').run(A_message.encode('utf-8').decode('utf-8'), podcast_path + f'/turno_{str(i)}_guest.mp3')

            if i > 0:
                elapsed_time = time.time() - start_time
                remaining_time = 22 - elapsed_time
                if remaining_time > 0:
                    time.sleep(remaining_time)

                img_input_prompt = """f'Genera un prompt para generar una imagen a partir del mensaje del usuario. Responde unicamente con las keywords en inglés para generar una imagen visualmente impactante y relacionadas con el texto.'"""
                episode.log(channel='user', modality='text', content=img_input_prompt, agent_id='A')
                img_prompt = LLMClientClass(model='gpt-4.1', temperature=1).run(episode, agent_id='A')
                image = DalleModelClass().predict(img_prompt)
                image.convert('RGB').save(podcast_path + '/' + f'image_{str(i)}.jpeg', format='JPEG')
                time.sleep(30)

        history = episode.history
        history = history[history['agent_id'] == 'A']
        messages_df = history[history['channel'] != 'system']

        # SAVE TEXT
        text_podcast = (messages_df['content'] + '\n').sum()
        with open(podcast_path + '/final_script.txt', "w", encoding="utf-8") as archivo:
            archivo.write(text_podcast)

        silencio = np.zeros(int(24000 * 1.0), dtype=np.float32)  # 1 segundo de silencio
        combinado = []

        for i in range(0, max_iter):
            audio, sr = sf.read(podcast_path + f'/turno_{str(i)}_int.mp3', dtype='float32')
            combinado.append(audio)
            combinado.append(silencio)
            audio, sr = sf.read(podcast_path + f'/turno_{str(i)}_guest.mp3', dtype='float32')
            combinado.append(audio)
            combinado.append(silencio)

        audio_final = np.concatenate(combinado)
        wav_path = podcast_path + '/final_audio.wav'
        sf.write(wav_path, audio_final, 24000)

        # VIDEO GENERATION
        audio = AudioFileClip(podcast_path + '/final_audio.wav')
        spec = []
        max_iter = 3
        delta = audio.duration / (max_iter - 2)
        for i in range(2, max_iter):
            spec.append((podcast_path + f'/image_{str(i)}.jpeg', delta * (i - 2), delta * (i + 1 - 2)))

        output_path = podcast_path + '/' + "final_video.mp4"
        fps = 24

        clips = []
        for ruta, t0, t1 in spec:
            dur = t1 - t0
            clip = ImageClip(ruta, duration=dur)
            clips.append(clip)

        video = concatenate_videoclips(clips, method="chain")
        if video.duration > audio.duration:
            video = video.subclipped(0, audio.duration)  # Use subclipped() instead
        else:
            video = video.with_duration(audio.duration)  # Use with_duration() instead

        video = video.with_audio(audio)
        video.write_videofile(output_path, fps=fps, codec="libx264", audio_codec="aac")