import os


def generate_entry(name):
    key = name.replace(" ", "")
    # Find all images matching the key, including .2, .3, etc.
    images_dir = os.path.join(os.path.dirname(__file__), "../../client/assets/images")
    image_files = [
        f for f in os.listdir(images_dir) if f.startswith(key) and f.endswith(".jpg")
    ]
    images = [f"/assets/images/{img}" for img in sorted(image_files)]
    return {
        "name": name,
        "images": images,
        "audio": f"/assets/audio/{key}.mp3",
        "transcripts": f"/assets/transcripts/{key}.json",
    }


# Auto-detect names from transcripts directory
transcripts_dir = os.path.join(
    os.path.dirname(__file__), "../../client/assets/transcripts"
)
transcript_files = [f for f in os.listdir(transcripts_dir) if f.endswith(".json")]
names = [os.path.splitext(f)[0] for f in transcript_files]

database = [generate_entry(name) for name in names]

print(f"Loaded {len(database)} entries from {transcripts_dir}")

from pprint import pprint

pprint(database)
