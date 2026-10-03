#!/usr/bin/env python3
"""Add the default UniFleet narration to the Global Airlines video."""

import json
import re
import subprocess
import tempfile
from pathlib import Path


SOURCE_VIDEO = Path("Global Airlines.mp4")
NARRATION_PAGE = Path("unifleet-narration.html")
OUTPUT_VIDEO = Path("video/global-airlines-with-narration.mp4")


def default_narration() -> str:
    html = NARRATION_PAGE.read_text(encoding="utf-8")
    match = re.search(
        r"default:\s*\{.*?narrationText:\s*\"([^\"]+)\"",
        html,
        flags=re.DOTALL,
    )
    if not match:
        raise SystemExit("Could not find the default narration in unifleet-narration.html")

    narration = match.group(1).replace("HPE", "H P E")
    return f"Hello everyone. Welcome. {narration}"


def source_has_audio() -> bool:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "a",
            "-show_entries",
            "stream=index",
            "-of",
            "json",
            str(SOURCE_VIDEO),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return bool(json.loads(result.stdout).get("streams"))


def main() -> None:
    if not SOURCE_VIDEO.is_file():
        raise SystemExit(f"Source video not found: {SOURCE_VIDEO}")

    OUTPUT_VIDEO.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temp_dir:
        narration_file = Path(temp_dir) / "narration.mp3"
        subprocess.check_call(
            [
                "edge-tts",
                "--voice",
                "en-GB-SoniaNeural",
                "--rate=-8%",
                "--text",
                default_narration(),
                "--write-media",
                str(narration_file),
            ]
        )

        command = [
            "ffmpeg",
            "-y",
            "-stream_loop",
            "-1",
            "-i",
            str(SOURCE_VIDEO),
            "-i",
            str(narration_file),
        ]
        if source_has_audio():
            command += [
                "-filter_complex",
                "[0:a]volume=0.16[background];"
                "[background][1:a]amix=inputs=2:duration=shortest:dropout_transition=2[audio]",
                "-map",
                "0:v:0",
                "-map",
                "[audio]",
            ]
        else:
            command += ["-map", "0:v:0", "-map", "1:a:0"]

        command += [
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "20",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            "-shortest",
            str(OUTPUT_VIDEO),
        ]
        subprocess.check_call(command)

    print(f"Wrote {OUTPUT_VIDEO}")


if __name__ == "__main__":
    main()
