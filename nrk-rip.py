import os
import os.path
import re
import shlex
import subprocess
import sys
from urllib.parse import urljoin, unquote

import requests

import ttml2srt


def sanitize_filename(filename):
    return filename.replace(":", "_").strip()


def sanitize_metadata(metadata):
    return metadata.replace("\n", "")

def stream_url_from_metadata(metadata, quality):
    quality_urls = {
        "video":
            {
                "high": "index_4_av.m3u8",
                "medium": "index_3_av.m3u8",
                "low": "index_2_av.m3u8"
            },
        "audio":
            {
                "high": "index_1_a.m3u8",
                "medium": "index_0_a.m3u8",  # Radio only has two qualities, so we let mediumm be low
                "low": "index_0_a.m3u8"
            }
    }
    media_url = metadata["mediaUrl"]
    idx = media_url.index("/z/")
    stream_url = media_url[:idx + 1] + "i" + media_url[idx + 2:]
    media_quality_urls = quality_urls[metadata["mediaType"].lower()]
    stream_url = urljoin(stream_url, media_quality_urls.get(quality, media_quality_urls["high"]))  # Defaults to high
    return stream_url


def subtitle_url_from_metadata(metadata):
    if metadata["mediaAssets"][0]["timedTextSubtitlesUrl"] is None:
        return None
    return unquote(metadata["mediaAssets"][0]["timedTextSubtitlesUrl"])


def metadata_from_media_id(media_id):
    element_url = "https://psapi-ne.nrk.no/mediaelement/%s" % media_id
    return requests.get(element_url).json()


def create_ffmpeg_command(stream_url, filename, subtitle_path=None, title=None, description=None):
    cmd = '-y -i "%s"' % stream_url
    if subtitle_path:
        cmd += ' -i "%s" -metadata:s:s:0 language=nor' % subtitle_path
    if title:
        cmd += ' -metadata title="%s"' % title
    if description:
        cmd += ' -metadata description="%s"' % description
    cmd += ' -c copy "%s"' % filename
    return cmd


def save_subtitle(metadata):
    media_id = metadata["id"]
    subtitle_url = subtitle_url_from_metadata(metadata)
    if not subtitle_url:
        return None
    ttml_doc = requests.get(subtitle_url).text
    subtitle_filename = "%s.srt" % media_id
    ttml2srt.ttml2srtfile(ttml_doc, subtitle_filename)
    return subtitle_filename


def media_id_from_url(url):
    match = re.match(".*/([A-Z\d]+?)/.*", url)
    return match.group(1)


def is_video(metadata):
    return metadata["mediaType"].lower() == "video"


def save_media(url, quality="high", verbose=False):
    media_id = media_id_from_url(url)
    metadata = metadata_from_media_id(media_id)
    subtitle_path = None
    stream_url = stream_url_from_metadata(metadata, quality)

    if is_video(metadata):
        # Download TTML subtitles and convert them to SRT
        subtitle_path = save_subtitle(metadata)
        cmd = create_ffmpeg_command(stream_url, sanitize_filename(metadata["fullTitle"]) + ".mkv", subtitle_path,
                                    metadata.get("title"), sanitize_metadata(metadata.get("description")))
    else:
        cmd = create_ffmpeg_command(stream_url, sanitize_filename(metadata["fullTitle"]) + ".aac",
                                    title=metadata.get("title"),
                                    description=sanitize_metadata(metadata.get("description")))
    run_ffmpeg(cmd, verbose=verbose)
    if os.path.exists(subtitle_path):
        os.remove(subtitle_path)


def run_ffmpeg(ffmpeg_args, verbose=False):
    # TODO: Add check for FFMPEG in path (shutil.which)
    cmd = "ffmpeg " + ffmpeg_args
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, b''):
        if verbose:
            print(line.decode(sys.stdout.encoding))
    p.stdout.close()
    return p.wait()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("URL", help="URL to NRK program")
    parser.add_argument("--quality", "-q", choices=["high", "medium", "low"])
    parser.add_argument("--verbose", "-V", action="store_true")
    args = parser.parse_args()
    save_media(args.URL, quality=args.quality, verbose=args.verbose)
