#!/usr/bin/env python3

# prerequisites: as described in https://alphacephei.com/vosk/install and also python module `sounddevice` (simply run command `pip install sounddevice`)
# Example usage with English model: `python test_microphone.py -m models/vosk-model-en-us`
# For more help run: `python test_microphone.py -h`

import argparse
import queue
import sys
import os
import sounddevice as sd
from vosk import Model, KaldiRecognizer

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="Show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="Audio file to store recording to")
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="Input device (numeric ID or substring)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="Sampling rate")
parser.add_argument(
    "-m", "--model", type=str, required=True,
    help="Path to the language model directory (e.g., models/vosk-model-en-us)")
args = parser.parse_args(remaining)

try:
    # Ensure the model path exists
    if not os.path.isdir(args.model):
        raise FileNotFoundError(f"Model directory does not exist: {args.model}")
    print(f"Loading model from: {args.model}")
    model = Model(args.model)

    # Get default sample rate if not specified
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        args.samplerate = int(device_info["default_samplerate"])

    # Open a file to dump audio data if specified
    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize=8000, device=args.device,
                           dtype="int16", channels=1, callback=callback):
        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)

        rec = KaldiRecognizer(model, args.samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                print(rec.Result())
            else:
                print(rec.PartialResult())
            if dump_fn is not None:
                dump_fn.write(data)

except KeyboardInterrupt:
    print("\nRecording stopped.")
    parser.exit(0)
except FileNotFoundError as e:
    print(f"Error: {e}")
    parser.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    parser.exit(1)
