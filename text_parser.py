import csv
import re
import json
from klpt.preprocess import Preprocess

class WordPair:
    def __init__(self):
        self.source_word = ""
        self.source_lang = ""
        self.source_def = ""
        self.kurdish_word = ""
        self.kurdish_def = ""
        self.sound_changes = []
        self.notes = []

def clean_text(text):
    # Remove HTML tags
    # text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&nbsp;', ' ')

    # Remove extra whitespace
    text = ' '.join(text.split())
    return text


def extract_word_and_definition(text):
    """Extract word and definition from a string like 'word (definition)'."""
    # Handle cases with Arabic/Kurdish script
    parts = text.split('(', 1)
    word = parts[0].strip()
    definition = ''
    if len(parts) > 1:
        definition = parts[1].rstrip(')').strip()

    # Clean up any remaining whitespace or special characters
    word = re.sub(r'\s+', ' ', word).strip()
    return word, definition


def parse_entry_group(lines):
    """Parse a group of related entries (between empty lines)."""
    pairs = []
    kurdish_line = None
    other_lines = []

    # First pass: categorize lines
    for line in lines:
        if not line.strip():
            continue
        if line.startswith('Kurdish:'):
            kurdish_line = line
        else:
            other_lines.append(line)

    # If we found both Kurdish and other languages, create pairs
    if kurdish_line and other_lines:
        # Extract Kurdish information
        kurdish_text = kurdish_line.replace('Kurdish:', '').strip()
        kurdish_word, kurdish_def = extract_word_and_definition(kurdish_text)

        # Create a pair for each non-Kurdish language
        for other_line in other_lines:
            pair = WordPair()

            # Extract source language and text
            lang_split = other_line.split(':', 1)
            if len(lang_split) == 2:
                pair.source_lang = lang_split[0].strip()
                source_text = lang_split[1].strip()
                pair.source_word, pair.source_def = extract_word_and_definition(source_text)

                # Add Kurdish information
                pair.kurdish_word = kurdish_word.split(' ')
                pair.kurdish_def = kurdish_def.split(' ')

                # Extract any potential sound changes
                # This is a placeholder - you might want to enhance this based on your specific needs
                sound_changes = re.findall(r'\b[a-z]+>[a-z]+\b', source_text + ' ' + kurdish_text)
                pair.sound_changes = sound_changes

                # Extract notes (anything in parentheses that isn't a definition)
                notes = re.findall(r'\(((?![^()]*>[^()]*)[^()]+)\)', source_text + ' ' + kurdish_text)
                pair.notes = [note.strip() for note in notes if note != pair.source_def and note != pair.kurdish_def]

                pairs.append(pair)

    return pairs


def extract_sound_changes(text):
    # Look for common patterns indicating sound changes
    changes = []
    patterns = [
        r'cf\.[^,)]*',
        r'\([^)]*>[^)]*\)',
        r'[a-z]>[a-z]'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        changes.extend(matches)
    
    return [c.strip() for c in changes if c.strip()]

def parse_entry(text):
    # Split into source and Kurdish parts
    parts = text.split("Kurdish:")
    if len(parts) != 2:
        return None
        
    pair = WordPair()
    
    # Parse source part
    source_part = parts[0].strip()
    source_langs = ["Urartian:", "Hurrian:", "Kassite:"]
    
    for lang in source_langs:
        if lang in source_part:
            pair.source_lang = lang.replace(":", "")
            pair.source_word = source_part.split(lang)[1].strip()
            break
    
    # Parse Kurdish part
    kurdish_part = parts[1].strip()
    
    # Extract Kurdish word and definition
    k_match = re.match(r'([^()]+)(?:\s*\(([^)]+)\))?', kurdish_part)
    if k_match:
        pair.kurdish_word = k_match.group(1).strip()
        if k_match.group(2):
            pair.kurdish_def = k_match.group(2).strip()
            
    # Extract sound changes
    pair.sound_changes = extract_sound_changes(kurdish_part)
    
    # Extract notes (anything in parentheses not related to sound changes)
    notes = re.findall(r'\((?!.*>)[^)]+\)', kurdish_part)
    pair.notes = [n.strip('()') for n in notes if '>' not in n]
    
    return pair


def parse_file(text):
    """Parse the entire file content."""
    # Split the text into groups (separated by double <br /> or empty lines)
    text = text.replace('<br />\n<br />', '\n\n')
    groups = text.split('\n\n')

    all_pairs = []
    for group in groups:
        if not group.strip():
            continue

        # Split group into lines and clean them
        lines = [clean_text(line) for line in group.split('<br />') if line.strip()]
        pairs = parse_entry_group(lines)
        all_pairs.extend(pairs)

    return all_pairs


# Example usage:
with open('preprocessed.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    pairs = parse_file(text)
    for pair in pairs:
        # pair.kurdish_word = ''.join(pair.kurdish_word)+';'
        # pair.kurdish_def = ''.join(pair.kurdish_def)+';'
        # pair.notes = ''.join(pair.notes)+';'
        print(f"Source Lang: {pair.source_lang}")
        print(f"Source Word: {pair.source_word}")
        print(f"Source Def: {pair.source_def}")
        print(f"Kurdish Word: {pair.kurdish_word}")
        print(f"Kurdish Def: {pair.kurdish_def}")
        print(f"Sound Changes: {pair.sound_changes}")
        print(f"Notes: {pair.notes}")
        print("---")


def export_to_json(pairs, filename):
    """
    Export WordPair objects to a JSON file.

    Args:
        pairs (list): List of WordPair objects.
        filename (str): Output file path.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump([pair.__dict__ for pair in pairs], f, ensure_ascii=False, indent=4)

"""
change the json to this:

{
    "source_word": {
      word: "",
      ipa_transcription: ""  # Not possible without more info; assume /ɑːle/
    },
  	"ipa_source_transcription":"/ɑːle/",
  	"source_lang":"Urartian",
  	"source_def":"he says",
  	"kurdish_word":[
  		{"word":"Ale","ipa_kurdish_transcription":"/ɑːle/"},
  		{"scripted_form":"","ipa_kurdish_transcription":"/ɑːle/"}
  		{"sئەڵێ":"","ipa_kurdish_transcription":"/ɑːle/"}
  		# Adjust based on actual pronunciation of  in Sorani script; e.g., /ælæ/
  	],
  	"kurdish_def":[["he"],["says"]],
  	"sound_changes":[],
  	note:[
  		note:"", 	
  	  ]
}
"""

def export_to_csv(pairs, filename):
    """
    Export WordPair objects to a CSV file.

    Args:
        pairs (list): List of WordPair objects.
        filename (str): Output file path.
    """
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(
            ['Source Lang', 'Source Word', 'Source Def', 'Kurdish Word', 'Kurdish Def', 'Sound Changes', 'Notes'])
        # Write data rows
        for pair in pairs:
            writer.writerow([
                pair.source_lang,
                pair.source_word,
                pair.source_def,
                pair.kurdish_word,
                pair.kurdish_def,
                ';'.join(pair.sound_changes),
                ';'.join(pair.notes)])


def export_to_markdown(pairs, filename):
    """
    Export WordPair objects to a Markdown file as a table.

    Args:
        pairs (list): List of WordPair objects.
        filename (str): Output file path.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        # Write table header
        f.write('| Source Lang | Source Word | Source Def | Kurdish Word | Kurdish Def | Sound Changes | Notes |\n')
        f.write('|-------------|-------------|------------|--------------|-------------|---------------|-------|\n')
        # Write table rows
        for pair in pairs:
            f.write(
                f'| {pair.source_lang} | {pair.source_word} | {pair.source_def} | {pair.kurdish_word} | {pair.kurdish_def} | {", ".join(pair.sound_changes)} | {", ".join(pair.notes)} |\n')




pairs = parse_file(text)
export_to_json(pairs, 'word_pairs.json')
export_to_csv(pairs, 'word_pairs.csv')
export_to_markdown(pairs, 'word_pairs.md')