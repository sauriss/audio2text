import pytest
from src.audio2text.transcribe import segments_to_srt, segments_to_vtt

FAKE_SEGMENTS = [
    {"start": 0.0, "end": 1.23, "text": "Hello world."},
    {"start": 1.24, "end": 2.50, "text": "This is a test."},
]

def test_segments_to_srt():
    srt = segments_to_srt(FAKE_SEGMENTS)
    assert "Hello world." in srt
    assert "This is a test." in srt
    assert "00:00:00,000" in srt

def test_segments_to_vtt():
    vtt = segments_to_vtt(FAKE_SEGMENTS)
    assert "WEBVTT" in vtt
    assert "Hello world." in vtt
    assert "00:00:00.000" in vtt

def test_import_and_cli():
    import src.audio2text.cli
    import src.audio2text.transcribe
