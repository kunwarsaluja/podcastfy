#!/usr/bin/env python3
"""
Generate one podcast from a single article URL and store outputs in:
  /Users/saluja/Desktop/WorkArea/Franklin/diyfire_podcasts/<article-slug>/
"""

from __future__ import annotations

import argparse
from pathlib import Path
from urllib.parse import urlparse

from podcastfy.client import generate_podcast


DEFAULT_OUTPUT_ROOT = Path("/Users/saluja/Desktop/WorkArea/Franklin/diyfire_podcasts")


def article_slug_from_url(url: str) -> str:
    parsed = urlparse(url.strip())
    path = parsed.path.strip("/")
    if not path:
        return "home"

    slug = path.split("/")[-1]
    if "." in slug:
        slug = slug.split(".")[0]
    return slug or "home"


def build_conversation_override(
    article_root: Path,
    tts_model: str,
    podcast_name: str | None,
    podcast_tagline: str | None,
) -> dict:
    config = {
        "podcast_name": podcast_name or "Our Podcast",
        "podcast_tagline": podcast_tagline or "A diyFIRE audio breakdown",
    }
    config["text_to_speech"] = {
        "default_tts_model": tts_model,
        "output_directories": {
            "transcripts": str(article_root / "transcripts"),
            "audio": str(article_root / "audio"),
        },
    }
    return config


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate podcast audio for one article URL into diyfire_podcasts/<article-slug>/",
    )
    parser.add_argument("--url", required=True, help="Article URL to process")
    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_OUTPUT_ROOT),
        help="Base output folder (default: /Users/saluja/Desktop/WorkArea/Franklin/diyfire_podcasts)",
    )
    parser.add_argument(
        "--tts-model",
        default="edge",
        choices=["edge", "openai", "elevenlabs", "gemini"],
        help="TTS model to use (default: edge)",
    )
    parser.add_argument(
        "--podcast-name",
        default="Our Podcast",
        help="Podcast name used in the intro line",
    )
    parser.add_argument(
        "--podcast-tagline",
        default="A diyFIRE audio breakdown",
        help="Podcast tagline used in the intro line",
    )
    args = parser.parse_args()

    article_slug = article_slug_from_url(args.url)
    article_root = Path(args.output_root).expanduser() / article_slug
    article_root.mkdir(parents=True, exist_ok=True)

    conversation_config = build_conversation_override(
        article_root,
        args.tts_model,
        args.podcast_name,
        args.podcast_tagline,
    )

    transcript_path = generate_podcast(
        urls=[args.url],
        tts_model=args.tts_model,
        transcript_only=True,
        conversation_config=conversation_config,
    )

    if not transcript_path:
        raise RuntimeError("Transcript generation did not return an output path.")

    transcript_target = article_root / "transcripts" / f"{article_slug}_transript.txt"
    Path(transcript_path).replace(transcript_target)

    audio_path = generate_podcast(
        transcript_file=str(transcript_target),
        urls=[args.url],
        tts_model=args.tts_model,
        conversation_config=conversation_config,
    )

    if not audio_path:
        raise RuntimeError("Audio generation did not return an output path.")

    audio_target = article_root / "audio" / f"{article_slug}.mp3"
    Path(audio_path).replace(audio_target)

    print(f"Article: {args.url}")
    print(f"Slug: {article_slug}")
    print(f"Output root: {article_root}")
    print(f"Transcript file: {transcript_target}")
    print(f"Audio file: {audio_target}")


if __name__ == "__main__":
    main()
