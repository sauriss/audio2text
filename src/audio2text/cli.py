import argparse
import sys
from .transcribe import run_transcription
import os

def main():
    parser = argparse.ArgumentParser(
        description="Convert audio to text using Whisper"
    )
    parser.add_argument("input", help="Input audio file (wav/mp3/aac/m4a)")
    parser.add_argument("--model", default="base", choices=["tiny", "base", "small", "medium", "large"], help="Whisper model size")
    parser.add_argument("--language", default="en", help="Language code (default: en)")
    parser.add_argument("--srt", action="store_true", help="Write SRT subtitle file")
    parser.add_argument("--vtt", action="store_true", help="Write VTT subtitle file")
    parser.add_argument("--out", help="Output basename (default: input filename)")

    args = parser.parse_args()

    input_path = args.input
    # Determine output basename:
    # - Use --out if provided
    # - Otherwise default to <OUTPUT_DIR>/<input_basename>
    #   where OUTPUT_DIR defaults to "output/target" and can be overridden
    #   by AUDIO2TEXT_OUTPUT_DIR env var.
    if args.out:
        basename = args.out
    else:
        output_dir = os.getenv("AUDIO2TEXT_OUTPUT_DIR", "output/target")
        input_basename = os.path.splitext(os.path.basename(input_path))[0]
        basename = os.path.join(output_dir, input_basename)

    try:
        out_files = run_transcription(
            input_path,
            model=args.model,
            language=args.language,
            write_srt=args.srt,
            write_vtt=args.vtt,
        )
        # Ensure output directory exists and move files to the desired location
        os.makedirs(os.path.dirname(basename), exist_ok=True)
        for ext, path in list(out_files.items()):
            new_path = f"{basename}.{ext}"
            # Skip rename if it's already the correct path
            if os.path.abspath(path) != os.path.abspath(new_path):
                os.replace(path, new_path)
            out_files[ext] = new_path
        print("Output files:")
        for ext, path in out_files.items():
            print(f"  {ext}: {path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
