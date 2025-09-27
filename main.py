from nicegui import ui, app
from pathlib import Path
import asyncio, uuid, subprocess
import numpy as np
import soundfile as sf
from kokoro import KPipeline

GENERATED_DIR = Path('generated')
GENERATED_DIR.mkdir(exist_ok=True)
SAVE_DEFAULT = str(GENERATED_DIR.resolve())

app.add_static_files('/generated', str(GENERATED_DIR))
app.add_static_files('/assets', 'assets')
app.native.window_args['title'] = 'KokoSpeak'

ui.add_css("""
html, body, #q-app, #app { height:100%; overflow:hidden; overscroll-behavior:none; }
.q-layout, .q-page-container, .q-page { height:100%; overflow:hidden; }
* { box-sizing:border-box; }
.no-resize { resize: none !important; }
audio::-webkit-media-controls-panel { background-color: rgba(0,0,0,0.92); }
audio::-webkit-media-controls-enclosure { border-radius: 12px; }
audio::-webkit-media-controls-current-time-display,
audio::-webkit-media-controls-time-remaining-display { color: #fff; }
audio::-webkit-media-controls-play-button,
audio::-webkit-media-controls-mute-button,
audio::-webkit-media-controls-timeline,
audio::-webkit-media-controls-volume-slider { filter: invert(1) hue-rotate(180deg); }
a:hover { color: #8A2BE2; }
""")

_pipeline = None
VOICE_OPTIONS = {'af_heart': 'F · Heart', 'af_bella': 'F · Bella', 'af_alloy': 'F · Alloy', 'am_adam': 'M · Adam'}
SPEED_OPTIONS = {'0.80': 0.80, '0.90': 0.90, '1.00': 1.00, '1.10': 1.10, '1.20': 1.20}
FORMAT_OPTIONS = {'wav': 'WAV', 'flac': 'FLAC', 'ogg': 'OGG', 'mp3': 'MP3'}

SILENCE = GENERATED_DIR / 'silence.wav'
if not SILENCE.exists():
    sf.write(SILENCE, np.zeros(2400, dtype='float32'), 24000)
SILENCE_URL = f'/generated/{SILENCE.name}'

def kokoro_generate(text: str, voice: str, speed: float):
    global _pipeline
    if _pipeline is None:
        _pipeline = KPipeline(lang_code='a')
    stream = _pipeline(text, voice=voice, speed=speed)
    chunks = []
    for item in stream:
        audio = item[-1]
        chunks.append(audio)
    if not chunks:
        return np.zeros(1, dtype='float32'), 24000
    return np.concatenate(chunks), 24000



def write_format(audio, sr, out_dir: Path, base: str, fmt: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    if fmt == 'wav':
        p = out_dir / f'{base}.wav'
        sf.write(p, audio, sr)
        return p
    if fmt == 'flac':
        p = out_dir / f'{base}.flac'
        sf.write(p, audio, sr, format='FLAC')
        return p
    if fmt == 'ogg':
        p = out_dir / f'{base}.ogg'
        sf.write(p, audio, sr, format='OGG', subtype='VORBIS')
        return p
    if fmt == 'mp3':
        wav_tmp = GENERATED_DIR / f'{base}_tmp.wav'
        sf.write(wav_tmp, audio, sr)
        p = out_dir / f'{base}.mp3'
        try:
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(wav_tmp), '-vn', '-ar', str(sr), '-ac', '1', '-b:a', '192k', str(p)], check=True)
        finally:
            wav_tmp.unlink(missing_ok=True)
        return p
    p = out_dir / f'{base}.wav'
    sf.write(p, audio, sr)
    return p

def synthesize(text: str, voice: str, speed: float, save_dir: str, fmt: str):
    audio, sr = kokoro_generate(text, voice, speed)
    base = uuid.uuid4().hex
    play_path = GENERATED_DIR / f'{base}.wav'
    sf.write(play_path, audio, sr)
    saved_path = write_format(audio, sr, Path(save_dir), base, fmt)
    return f'/generated/{play_path.name}', str(saved_path)

with ui.element('div').classes('fixed inset-0'):
    ui.element('div')\
      .classes('absolute inset-0 bg-cover bg-center bg-no-repeat hue-rotate-0')\
      .style('background-image: url(/assets/backgroundImage.gif)')
    ui.element('div').classes('absolute inset-0 bg-black/15 backdrop-blur md:backdrop-blur-md lg:backdrop-blur-xl pointer-events-none')

    with ui.element('div').classes('relative z-10 flex flex-col w-full p-10'):
        with ui.element('div').classes('w-full pb-3'):
            ui.label('KokoSpeak').classes('text-white font-bold text-2xl sm:text-5xl md:text-6xl lg:text-8xl')
            ui.label('Using open-sourced AI, Kokoro').classes('text-white/90 font-semibold text-xs sm:text-lg md:text-xl')

        with ui.element('div').classes('flex-1 w-full flex'):
            with ui.element('div').classes('bg-blend-multiply bg-black/60 rounded-xl backdrop-blur-md w-full p-5 gap-5 flex-1 flex min-h-0 overflow-hidden'):
                with ui.element('div').classes('flex flex-1 min-h-0 min-w-0 flex-col sm:flex-row gap-4'):
                    with ui.element('div').classes('flex-1 min-w-0 flex min-h-0 flex-col gap-3'):
                        ui.label('Prompt / Text').classes('text-white font-semibold text-base sm:text-2xl')
                        with ui.scroll_area().classes('flex-1 min-w-0 w-full rounded-md bg-black/90 p-2 min-h-0'):
                            text_box = ui.textarea(placeholder='Type something...').props('dark color=purple-12 autogrow input-class="no-resize text-white" input-style="overflow:hidden"').classes('w-full')
                        with ui.element('div').classes('flex gap-3 w-full'):
                            gen_btn = ui.button('Generate').props('color=black unelevated').classes('text-white flex-1')
                            clr_btn = ui.button('Clear').props('color=black unelevated').classes('text-white flex-1')

                    with ui.element('div').classes('flex-1 min-w-0 flex min-h-0 flex-col gap-3'):
                        ui.label('Audio Preview').classes('text-white font-semibold text-base sm:text-2xl')

                        with ui.expansion('Voice', value=False).classes('bg-black/80 text-white rounded-md'):
                            with ui.row().classes('w-full gap-4'):
                                voice_select = ui.select(
                                    options=VOICE_OPTIONS, value='af_heart', label='Voice'
                                ).classes('min-w-[12rem] text-white').props(
                                    'outlined dense dark popup-content-class="bg-black text-white" input-class="text-white"'
                                )

                        with ui.expansion('Speed', value=False).classes('bg-black/80 text-white rounded-md'):
                            with ui.row().classes('w-full gap-4'):
                                speed_select = ui.select(
                                    options=list(SPEED_OPTIONS.keys()), value='1.00', label='Speed'
                                ).classes('min-w-[10rem] text-white').props(
                                    'outlined dense dark popup-content-class="bg-black text-white" input-class="text-white"'
                                )

                        with ui.expansion('Output & Save', value=False).classes('bg-black/80 text-white rounded-md'):
                            with ui.grid(columns=2).classes('w-full gap-4'):
                                    format_select = ui.select(
                                        options=FORMAT_OPTIONS, value='wav', label='Format'
                                    ).classes('w-full text-white').props(
                                        'outlined dense dark popup-content-class="bg-black text-white" input-class="text-white"'
                                    )
                                    with ui.row().classes('w-full'):
                                        dir_input = ui.input(label='Directory', value=SAVE_DEFAULT).classes('w-full text-white').props('outlined dense dark input-class="text-white"')
                            with ui.element('div').classes('w-full flex gap-3'):
                                        folder_btn = ui.button('Folder').props('color=black unelevated').classes('text-white flex-1')
                                        def_btn = ui.button('Default').props('color=black unelevated').classes('text-white flex-1')

                        with ui.element('div').classes('w-full rounded-md bg-black/90 p-3'):
                            audio_el = ui.audio(src=SILENCE_URL).props('controls controlslist="nodownload noplaybackrate noremoteplayback" preload=auto').classes('w-full')
                            status = ui.label('').classes('text-white/70 text-sm whitespace-normal overflow-wrap-anywhere break-words')

                async def on_generate():
                    txt = (text_box.value or '').replace('\n', ' ')
                    if not txt:
                        status.text = 'Please enter some text.'
                        return
                    v = voice_select.value or 'af_heart'
                    s = SPEED_OPTIONS.get(str(speed_select.value), 1.0)
                    f = format_select.value or 'wav'
                    d = dir_input.value or SAVE_DEFAULT
                    gen_btn.disable()
                    status.text = 'Generating…'
                    try:
                        play_url, saved_path = await asyncio.to_thread(synthesize, txt, v, s, f'{d}', f)
                        audio_el.set_source(play_url if play_url else SILENCE_URL)
                        status.text = f'Saved: {saved_path}'
                    except Exception as e:
                        audio_el.set_source(SILENCE_URL)
                        status.text = f'Error: {e}'
                    finally:
                        gen_btn.enable()

                def on_clear():
                    text_box.value = ''
                    audio_el.set_source(SILENCE_URL)
                    status.text = ''

                gen_btn.on_click(on_generate)
                clr_btn.on_click(on_clear)

ui.run(native=True, reload=False)
