def stt_tool(config):
    import io, tempfile, time, threading, warnings
    import numpy as np, sounddevice as sd, soundfile as sf, keyboard, pyperclip
    engine = config.get('engine', 'local'); hotkey = config.get('hotkey', 'ctrl+shift+r')
    sr = int(config.get('samplerate', 48000)); ch = int(config.get('channels', 1))
    bg = bool(config.get('run_in_background', False))
    try:
        from eigenlib.audio.oai_whisper_stt import OAIWhisperSTTClass
    except Exception as e:
        warnings.warn(f'cloud engine no disponible: {e}'); OAIWhisperSTTClass = None
    def record():
        stop = {'v': False}; frames = []
        def cb(indata, *_):
            frames.append(indata.copy());
            (_ for _ in ()).throw(sd.CallbackStop()) if stop['v'] else None
        with sd.InputStream(samplerate=sr, channels=ch, callback=cb):
            while not stop['v']: sd.sleep(100)
        buf = io.BytesIO(); sf.write(buf, np.concatenate(frames), sr, format='WAV'); return buf.getvalue()
    def transcribe(wav):
        if engine == 'cloud' and OAIWhisperSTTClass:
            with tempfile.NamedTemporaryFile(suffix='.wav') as f:
                f.write(wav); f.flush(); return OAIWhisperSTTClass().run(f.name, 'cloud').strip()
        import whisper; m = whisper.load_model('base')
        with tempfile.NamedTemporaryFile(suffix='.wav') as f:
            f.write(wav); f.flush(); return m.transcribe(f.name)['text'].strip()
    def paste(t):
        if t: pyperclip.copy(t); time.sleep(0.05); keyboard.press_and_release('ctrl+v')
    rec = {'on': False}
    def hk():
        if rec['on']: return
        rec['on'] = True; stop = {'v': False}
        def stop_hk(): stop['v'] = True
        sid = keyboard.add_hotkey(hotkey, stop_hk, trigger_on_release=True)
        wav = record()
        keyboard.remove_hotkey(sid); rec['on'] = False
        try: paste(transcribe(wav))
        except Exception as e: print('STT error:', e)
    keyboard.add_hotkey(hotkey, hk, trigger_on_release=True)
    runner = lambda: keyboard.wait()
    if bg:
        t = threading.Thread(target=runner, daemon=True); t.start(); config['result']={'background':True,'thread':t}
    else:
        runner(); config['result']={'background':False}
    return config
