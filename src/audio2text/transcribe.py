import os
import logging
from typing import List, Dict
import whisper

def segments_to_srt(segments: List[Dict]) -> str:
    def format_timestamp(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    lines = []
    for i, seg in enumerate(segments, 1):
        lines.append(str(i))
        lines.append(f"{format_timestamp(seg['start'])} --> {format_timestamp(seg['end'])}")
        lines.append(seg['text'].strip())
        lines.append("")
    return "\n".join(lines)

def segments_to_vtt(segments: List[Dict]) -> str:
    def format_timestamp(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{h:02}:{m:02}:{s:02}.{ms:03}"

    lines = ["WEBVTT\n"]
    for seg in segments:
        lines.append(f"{format_timestamp(seg['start'])} --> {format_timestamp(seg['end'])}")
        lines.append(seg['text'].strip())
        lines.append("")
    return "\n".join(lines)

def run_transcription(
    input_path: str,
    model: str = "base",
    language: str = "en",
    write_srt: bool = False,
    write_vtt: bool = False,
) -> dict:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    logger = logging.getLogger("audio2text")

    if not os.path.isfile(input_path):
        logger.error(f"Input file not found: {input_path}")
        raise FileNotFoundError(f"Input file not found: {input_path}")

    logger.info(f"Loading Whisper model: {model}")
    # Allow overriding model location via env var (e.g., repo's ./models or a shared dir)
    models_dir = os.getenv("AUDIO2TEXT_MODELS_DIR")
    model_arg = model
    if models_dir:
        candidate = os.path.join(models_dir, f"{model}.pt")
        if os.path.isfile(candidate):
            logger.info(f"Using local model checkpoint: {candidate}")
            model_arg = candidate
        else:
            logger.info(
                f"AUDIO2TEXT_MODELS_DIR set but no '{model}.pt' found in {models_dir}; falling back to default download/cache"
            )

    try:
        wmodel = whisper.load_model(model_arg)
    except Exception as e:
        logger.error(f"Failed to load model '{model}': {e}")
        raise

    logger.info(f"Transcribing '{input_path}' (language={language})")
    try:
        result = wmodel.transcribe(input_path, language=language)
    except whisper.audio.FFMPEGNotFoundError:
        logger.error("ffmpeg not found. Please install ffmpeg and ensure it's in your PATH.")
        raise
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        raise

    segments = result.get("segments", [])
    text = result.get("text", "").strip()
    basename = os.path.splitext(os.path.basename(input_path))[0]
    out_files = {}

    txt_path = f"{basename}.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    out_files["txt"] = txt_path
    logger.info(f"Transcript written to {txt_path}")

    if write_srt:
        srt_path = f"{basename}.srt"
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(segments_to_srt(segments))
        out_files["srt"] = srt_path
        logger.info(f"SRT written to {srt_path}")

    if write_vtt:
        vtt_path = f"{basename}.vtt"
        with open(vtt_path, "w", encoding="utf-8") as f:
            f.write(segments_to_vtt(segments))
        out_files["vtt"] = vtt_path
        logger.info(f"VTT written to {vtt_path}")

    duration = result.get("duration")
    if duration:
        logger.info(f"Audio duration: {duration:.2f} seconds")

    return out_files
