# README.md

## audio2text(mac os)

Convert audio files (wav/mp3/aac/m4a) to text using local Whisper (OpenAI) and ffmpeg.

### Features

- CLI tool: `audio2text`  
- Outputs: transcript (`.txt`), optional subtitles (`.srt`, `.vtt`)
- Select model size: `--model` (tiny/base/small/medium/large)
- Language: default English, override with `--language`
- Robust logging and error messages

### Prerequisites

- Python 3.10+
- ffmpeg (macOS: `brew install ffmpeg`)

### Quick Start

```sh
# 1) Install ffmpeg (macOS)
brew install ffmpeg

# 2) Create and activate a virtualenv
python3 -m venv .venv && source .venv/bin/activate

# 3) Install dependencies and the package
pip install -U pip && pip install -r requirements.txt && pip install .

# 4) Transcribe an audio file (writes .txt and, with --srt, .srt)
# By default, outputs go under output/target/<input-basename>.*
audio2text /path/to/audio.wav --srt --model base
```

### Models

- By default, Whisper downloads models to a cache (typically `~/.cache/whisper`).
- You can keep project-specific or shared checkpoints in a dedicated folder and point the app to it.

Options:
- Use repo models folder:
  - Create `models/` (already in repo, git-ignored) and place files like `base.pt`, `small.pt`.
  - Export `AUDIO2TEXT_MODELS_DIR` to use local checkpoints:
    - `export AUDIO2TEXT_MODELS_DIR="$PWD/models"`
    - Or with direnv: add `export AUDIO2TEXT_MODELS_DIR=./models` in `.envrc` and run `direnv allow`.
- Centralize caches:
  - Set `XDG_CACHE_HOME="$HOME/Dev/models/.cache"` to keep Whisper downloads under that path.

### Run Examples

```sh
# Default English transcription, write transcript + SRT under output/target
audio2text /path/to/audio.m4a --srt --model base

# Also write VTT
audio2text /path/to/audio.aac --srt --vtt --model base

# Faster first run (smaller model download)
audio2text /path/to/audio.mp3 --srt --model tiny

# Example with absolute paths
source ~/path/to/audio2text/.venv310/bin/activate \
  && audio2text /path/to/output-o.aac --srt
```

Run without installing the package (optional):
```sh
PYTHONPATH=src python3 -m audio2text /path/to/audio.wav --srt --model base

### Output Location

- Default: outputs are written under `output/target/<input-basename>.*` relative to the current working directory.
- Override the directory with `--out` to provide a full basename:
  - `audio2text input.wav --out /path/to/myname` → writes `/path/to/myname.txt` (and `.srt/.vtt`)
- You can also set a default via env var:
  - `export AUDIO2TEXT_OUTPUT_DIR=/path/to/output/dir` (used when `--out` is not provided)
```

### Docker

```sh
docker build -t audio2text .
docker run --rm -v "$PWD:/work" audio2text audio2text /work/sample.wav --srt
```

### Notes

- Larger models are more accurate but slower.
- Set `--language` for non-English audio.
- Uses CPU by default; GPU if available (no CUDA setup steps here).
 - If `AUDIO2TEXT_MODELS_DIR` is set and contains `<model>.pt`, it is used; otherwise the model is downloaded and cached.
 - Outputs are written to your current working directory unless you pass `--out`.

### Troubleshooting

- **ffmpeg not found**: Install ffmpeg (`brew install ffmpeg` on macOS).
- **Codec errors**: Check input file format and ffmpeg support.
- **Large files**: Use a powerful machine or smaller model.
 - **ModuleNotFoundError: audio2text**: Make sure you ran `pip install .` in the active venv, or use the `PYTHONPATH=src ...` form.
 - **command not found: audio2text**: Activate the venv first: `source .venv/bin/activate`.

---
