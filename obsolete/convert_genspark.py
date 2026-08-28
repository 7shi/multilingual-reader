# Pull-style parser that extracts dialogue data from HTML files
# Reads per-speaker utterances from the given file, converts, and outputs them

import argparse

parser = argparse.ArgumentParser(description="Translate French dialogue text into English and Japanese")
parser.add_argument("input_file", help="Input file")
parser.add_argument("-o", "--output", required=True, help="Output file")
parser.add_argument("--speaker", default="A,B", help="Speaker names, comma-separated (e.g. Camille,Luc)")
args = parser.parse_args()

from xml7shi import reader

def normalize(text):
    # Text normalization: convert newlines/tabs to spaces and collapse consecutive spaces into one
    import re
    return re.sub(r'\s+', ' ', text.strip())

# Parse speaker names
speakers = args.speaker.split(",")
if len(speakers) != 2:
    raise ValueError("Exactly 2 speakers are required (e.g. --speaker Camille,Luc)")
speaker1, speaker2 = speakers

# Read the HTML file
with open(args.input_file, "r", encoding="utf-8") as f:
    html = f.read()

# Open the output file
with open(args.output, "w", encoding="utf-8") as f:
    # Parse HTML with a pull-style XML reader
    xr = reader(html)
    while xr.read():
        # Identify the speaker from div tags
        if xr.tag == "div":
            cls = xr["class"].split()
            if "speaker-color-1" in cls:
                speaker = speaker1
            elif "speaker-color-2" in cls:
                speaker = speaker2
        # Output the utterance content from span tags
        elif xr.tag == "span" and xr["class"] == "content" and xr.read():
            print(speaker + ":", normalize(xr.text), file=f)
