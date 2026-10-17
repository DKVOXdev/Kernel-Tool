# Copyright (c) Kernel-Tool
# See the file 'LICENSE' for copying permission
# ------------------------------------------------------------------------------------------------
# EN:
#     - Do not touch or modify the code below. If there is an error, please contact the owner,
#       but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR:
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le
#       propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.
# ------------------------------------------------------------------------------------------------

import os
import asyncio
import time
from pathlib import Path
from Config.Config import fakevoice_banner

LC = "\033[38;2;0;200;255m"
RS = "\033[0m"

try:
    import edge_tts
except ImportError:
    print(f'{LC}[ERROR] edge-tts not installed. Run: pip install edge-tts{RS}')
    exit(1)

OUTPUT_DIR = Path('output')
OUTPUT_DIR.mkdir(exist_ok=True)

FEMALE_VOICES = {
    'eloise': 'fr-FR-EloiseNeural',
    'denise': 'fr-FR-DeniseNeural',
    'sylvie': 'fr-CA-SylvieNeural',
    'sexy':   'fr-FR-DeniseNeural',
}

_AVAILABLE_VOICES = None


async def _get_available_voices():
    global _AVAILABLE_VOICES
    if _AVAILABLE_VOICES is not None:
        return _AVAILABLE_VOICES
    try:
        voices = await edge_tts.list_voices()
        _AVAILABLE_VOICES = {v.get('ShortName') for v in voices if v.get('ShortName')}
    except Exception:
        _AVAILABLE_VOICES = set()
    return _AVAILABLE_VOICES


def play_audio(filepath):
    try:
        os.startfile(filepath)
    except Exception as e:
        print(f'{LC}[ERROR] Could not play file: {e}{RS}')


async def generate_voice(text, voice_key='eloise'):
    print(f'{LC}[GENERATING] Synthesizing voice: "{text}"{RS}')

    voice = FEMALE_VOICES.get(voice_key, FEMALE_VOICES['eloise'])
    available = await _get_available_voices()

    if available and voice not in available:
        print(f'{LC}[WARN] Voice "{voice}" unavailable. Falling back to EloiseNeural.{RS}')
        voice = 'fr-FR-EloiseNeural'

    filename = OUTPUT_DIR / f'fakevoice_{int(time.time())}.mp3'

    rate_map  = {'sexy': '-15%', 'denise': '-5%'}
    pitch_map = {'sexy': '-2Hz', 'denise': '+2Hz'}
    rate  = rate_map.get(voice_key, '-10%')
    pitch = pitch_map.get(voice_key, '+8Hz')

    if voice_key == 'sexy':
        print(f'{LC}[SEXY MODE] Sensual adult voice activated...{RS}')

    try:
        comm = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
        await comm.save(str(filename))
        print(f'{LC}[OK] File saved: {filename}{RS}')
        print(f'{LC}[PLAYBACK] Playing...{RS}')
        play_audio(str(filename))

    except Exception as e:
        if 'No audio was received' in str(e) and voice != 'fr-FR-EloiseNeural':
            print(f'{LC}[WARN] No audio received. Retrying with EloiseNeural...{RS}')
            try:
                fb = edge_tts.Communicate(text=text, voice='fr-FR-EloiseNeural', rate='-5%', pitch='+2Hz')
                await fb.save(str(filename))
                print(f'{LC}[OK] File saved: {filename}{RS}')
                play_audio(str(filename))
            except Exception as e2:
                print(f'{LC}[ERROR] {e2}{RS}')
        else:
            print(f'{LC}[ERROR] {e}{RS}')


def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(coro)
    finally:
        loop.close()


def main():
    print(fakevoice_banner)
    print(f'{LC}{"═"*50}{RS}')
    print(f'{LC}   FAKE VOICE GENERATOR — ADULT FEMALE VOICE{RS}')
    print(f'{LC}{"═"*50}{RS}')
    print(f'{LC}\n Voice Options:{RS}')
    print(f'{LC}  1. Young Natural Voice (Eloise) — RECOMMENDED{RS}')
    print(f'{LC}  2. Natural Voice (Denise){RS}')
    print(f'{LC}  3. Quebec Voice (Sylvie) — Very Natural{RS}')
    print(f'{LC}  4. SEXY Adult Voice{RS}')

    choice = input(f'\n{LC}Choose voice (1-4) [1] → {RS}').strip() or '1'
    voice_map = {'1': 'eloise', '2': 'denise', '3': 'sylvie', '4': 'sexy'}
    voice_key = voice_map.get(choice, 'eloise')

    print(f'\n{LC}{"─"*50}{RS}')
    text = input(f'{LC} Enter text: {RS}').strip()
    print(f'{LC}{"─"*50}{RS}')

    if not text:
        print(f'{LC} Text cannot be empty!{RS}')
    else:
        run_async(generate_voice(text, voice_key))
        again = input(f'\n{LC} Generate another? (y/n) [n] → {RS}').lower()
        if again == 'y':
            main()
        else:
            print(f'\n{LC} Goodbye!{RS}')


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n\n{LC} Stopped.{RS}')
    except Exception as e:
        print(f'{LC}[ERROR] {e}{RS}')
