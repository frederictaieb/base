import spacy
import json
import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline
from pprint import pprint
import logging
import numpy as np
import matplotlib.colors as mcolors
import mimetypes
import shutil
import os
import uuid
import io
import tempfile
import asyncio
import mimetypes
import shutil
from pydantic import BaseModel
from typing import Dict
import logging
import re
import spacy
import requests
from app.config.logging_config import setup_logging
from app.services.storage.ipfs.ipfs_upload import upload_file
from app.services.storage.ipfs.ipfs_download import download_file
from app.services.storage.xrp.xrp_emitter import xrp_emitter



setup_logging()
logger = logging.getLogger(__name__)

# Emotion color and order definitions (from report.py)
EMOTION_COLORS = {
    'disgust': '#00FF00',   # vert
    'surprise': '#4B0082', # indigo
    'joy': '#FFFF00',      # jaune
    'sadness': '#0000FF',  # bleu
    'fear': '#FFA500',     # orange
    'anger': '#FF0000',    # rouge
    'neutral': '#800080'   # violet
}

EMOTION_ORDER = ['neutral', 'surprise', 'sadness', 'disgust', 'joy', 'fear', 'anger']

# Clean text from file and return a string
async def scrub(file):
    contents = await file.read()
    text = contents.decode("utf-8", errors="replace")
    # Supprime les séquences échappées et les caractères de contrôle
    text = text.replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "")
    text = text.replace("\\", "")  # Supprime les antislashs restants
    # Supprime les caractères de contrôle Unicode invisibles (excepté \n et \t)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    # Remplace les tabulations par un espace, supprime les doublons d'espaces
    text = text.replace("\t", " ")
    text = re.sub(r' +', ' ', text)
    # Nettoie les espaces superflus autour des sauts de ligne
    text = re.sub(r' *\n *', '\n', text)
    logger.info(f"*** SCRUB: {text} *** ")
    return text.strip()

# Split text into phrases
async def to_phrases(text: str) -> list[str]:
    nlp = spacy.load("en_core_web_sm") 
    doc = nlp(text)
    phrases = [sent.text.strip() for sent in doc.sents]
    return phrases

# TO SUMMARY
# Take a text
# Return a summary
async def text_to_summary(text: str) -> str:
    if len(text.split()) < 30:
        logger.info(f"*** SUMMARY: {text} ***")
        return {"summary": text}  # texte trop court à résumer

    prompt = (
        "Make a summary of the text between acolades: "
        + "{" + text + "}"
        + "Make it short, simple and anonymous."
        + "Remove firsname and lastname."
        + "Return only the summary, no other text."
    )

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",  # ou "openhermes", "llama2", etc.
                "prompt": prompt,
                "stream": False
            },
            timeout=120  # Timeout large pour long résumé
        )
        response.raise_for_status()
        generated = response.json()["response"].strip()
        logger.info(f"*** SUMMARY: {generated} ***")
        return {"summary": generated}

    except requests.exceptions.RequestException as e:
        return {"summary": f"Erreur lors de la génération via Ollama: {e}"}

# TO SUMMARY
# Take a file
# Return a summary
async def textfile_to_summary(file) -> list[str]:
    text = await scrub(file)
    return await text_to_summary(text)

# format IA Answer to a list of 3 sentences
# Take a text
# Return a list of 3 sentences
def extract_wisdom_list(text: str) -> list[str]:
    # Try to match numbered sentences, with or without quotes
    numbered = re.findall(r'\d+\.\s*["""]?(.*?)["""]?(?:\n|$)', text)
    if numbered:
        return [s.strip() for s in numbered if s.strip()][:3]

    # Try to match bulleted or dashed lists
    bulleted = re.findall(r'[-•—–]\s*["""]?(.*?)["""]?(?:\n|$)', text)
    if bulleted:
        return [s.strip() for s in bulleted if s.strip()][:3]

    # Fallback: split by newlines, filter out empty lines, and take up to 3
    lines = [line.strip("-•—– ").strip() for line in text.splitlines() if line.strip()]
    if lines:
        return lines[:3]

    # Final fallback: try to split by period if all else fails
    sentences = [s.strip() for s in re.split(r'[.?!]\s+', text) if s.strip()]
    return sentences[:3]

# TO WISDOM
# Take a text
# Return a list of 3 sentences
async def text_to_wisdom(text: str) -> list[str]:
    prompt = (
        "In the text between curly braces, find a maximum of 3 important phrases, full of wisdom and lessons about life:\n"
        f"{{{text}}}\n"
        "Return between 0 and 3 sentences, no other text.\n"
        "Keep anonymous by replacing any names with appropriate pronouns.\n"
        "Format the result as numbered sentences like:\n"
        "1. \"First sentence\"\n2. \"Second sentence\"\n3. \"Third sentence\""
    )

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        generated = response.json()["response"].strip()

        wisdom_list = extract_wisdom_list(generated)
        logger.info(f"*** WISDOM: {wisdom_list} ***")
        return {"wisdom": wisdom_list}

    except requests.exceptions.RequestException as e:
        return {"wisdom": f"Erreur lors de la génération via Ollama: {e}"}

# TO WISDOM
# Take a file
# Return a list of 3 sentences
async def textfile_to_wisdom(file) -> list[str]:
    text = await scrub(file)
    return await text_to_wisdom(text)

# TO EMOTIONS
# Take a text
# Return a list of emotions
async def text_to_emotions(text: str) -> list[str]:
    json_lines = []
    classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=7)
    
    phrases = await to_phrases(text)

    for phrase in phrases:
        logger.info(f"*** PHRASE: {phrase} ***")
        phrase = phrase.strip()
        if not phrase:
            continue

        results = classifier(phrase)[0]
        json_line = {
            "emotions": [{"label": res["label"], "score": res["score"]} for res in results]
        }
        json_lines.append(json_line)

    logger.info(f"*** TO EMOTIONS: {json_lines} ***")
    return {"emotions": json_lines}
 
# TO EMOTIONS
# Take a file
# Return a list of emotions
async def textfile_to_emotions(file) -> list[str]:
    text = await scrub(file)
    return await text_to_emotions(text)

# Process data from json to dataframe
# Take a list of emotions
# Return a dataframe
def process_data_json(data):
    rows = []
    for i, entry in enumerate(data):
        for emo in entry["emotions"]:
            rows.append({
                "index": i,
                "emotion": emo["label"],
                "score": emo["score"]
            })
    df = pd.DataFrame(rows)
    return df

# Analyze emotions
# Take a dataframe
# Return a dataframe with dominant emotion
def analyze_emotions(df):
    pivot = df.pivot(index="index", columns="emotion", values="score").fillna(0)
    pivot["dominant"] = pivot.idxmax(axis=1)
    return pivot

# Interpolate color
# Take a color and a score
# Return a color
def interpolate_color(color_hex, score, pale_factor=0.8):
    color_rgb = np.array(mcolors.to_rgb(color_hex))
    white_rgb = np.array([1, 1, 1])
    pale_rgb = white_rgb * pale_factor + color_rgb * (1 - pale_factor)
    result_rgb = pale_rgb * (1 - score) + color_rgb * score
    return result_rgb

# TO HEATMAP
# Take a list of emotions
# Return a heatmap
def text_to_heatmap(emotions, output_path="heatmap.png", to_save=True):
    logger.info(f"*** SHADER: {emotions} ***")

    df_long = process_data_json(emotions)
    df_wide = analyze_emotions(df_long)

    if "dominant" in df_wide.columns:
        data = df_wide.drop(columns="dominant")
    else:
        data = df_wide
    emotions = [e for e in EMOTION_ORDER if e in data.columns]
    data = data[emotions]
    n_emotions = len(emotions)
    n_phrases = data.shape[0]
    img = np.ones((n_emotions, n_phrases, 3))
    for i, emo in enumerate(emotions):
        color = EMOTION_COLORS.get(emo, '#000000')
        for j in range(n_phrases):
            score = data.iloc[j][emo]
            img[i, j, :] = interpolate_color(color, score)
    if to_save:
        plt.imsave(output_path, img)
        logging.info(f"Heatmap saved at {output_path}")
        return output_path
    else:
        buffer = io.BytesIO()
        plt.imsave(buffer, img, format='png')
        buffer.seek(0)
        return buffer

# TO TXT TO EMO
# Take a file
# Return a dictionary with summary, wisdom and emotions
async def textfile_to_heatmap(file):
    texte = await scrub(file)
    emotions = await text_to_emotions(texte)
    return text_to_heatmap(emotions.get("emotions"), to_save=False)

# TO TXT TO EMO
# Take a file
# Return a dictionary with summary, wisdom and emotions
async def textfile_to_emo(file, longitude, latitude, timestamp):

    id = str(uuid.uuid4())
    temp_dir = tempfile.mkdtemp(prefix=id)

    texte = await scrub(file)

    summary = await text_to_summary(texte)
    wisdom = await text_to_wisdom(texte)
    emotions = await text_to_emotions(texte)

    data =  {
        "timestamp": timestamp,
        "location": {
            "longitude": longitude,
            "latitude": latitude
        },
        "summary": summary.get("summary"), 
        "wisdom": wisdom.get("wisdom"),
        "emotions": emotions.get("emotions")
    }

    logger.info(f"*** DATA: {data} ***")

    json_path = os.path.join(temp_dir, "result.json")
    with open(json_path, "w") as f:
        json.dump(data, f)
    json_hash = upload_file(json_path)
    logger.info(f"*** JSON HASH: {json_hash} ***")

    heatmap_path = os.path.join(temp_dir, "heatmap.png")
    text_to_heatmap(emotions.get("emotions"), output_path=heatmap_path, to_save=True)
    heatmap_hash = upload_file(heatmap_path)
    logger.info(f"*** HEATMAP HASH: {heatmap_hash} ***")

    asyncio.create_task(asyncio.to_thread(xrp_emitter, json_hash, heatmap_hash))
    #xrp_emitter(json_hash, heatmap_hash)

    shutil.rmtree(temp_dir)

    return {
        "json_hash": json_hash,
        "heatmap_hash": heatmap_hash
    }
