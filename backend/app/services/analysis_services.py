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

import mimetypes
import shutil
import os

from pydantic import BaseModel
from typing import Dict

import logging
import re
from segtok import tokenizer
from segtok.segmenter import split_single
import requests

from app.config.logging_config import setup_logging

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

# TO LINES
async def scrub(file):
    logger.info(f"Cleaning file: {file.filename}")
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
    return text.strip()

async def to_phrases(file):
    texte = await scrub(file)
    # Découpe en phrases avec segtok
    phrases = [p.strip() for p in split_single(texte) if p.strip()]
    return {"phrases": phrases}


# TO SUMMARY
async def to_summary(text: str) -> str:
    if len(text.split()) < 30:
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
        return {"summary": generated}

    except requests.exceptions.RequestException as e:
        return {"summary": f"Erreur lors de la génération via Ollama: {e}"}

# TO WISDOM
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

async def to_wisdom(text: str) -> list[str]:
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
        logger.info(f"Generated wisdom: {generated}")

        wisdom_list = extract_wisdom_list(generated)
        logger.info(f"Extracted wisdom: {wisdom_list}")
        return {"wisdom": wisdom_list}

    except requests.exceptions.RequestException as e:
        return {"wisdom": f"Erreur lors de la génération via Ollama: {e}"}


async def txt_to_emo(file):
    texte = await scrub(file)
    summary = await to_summary(texte)
    wisdom = await to_wisdom(texte)
    return {"summary": summary.get("summary"), "wisdom": wisdom.get("wisdom")}
    
def generate_emotional_report_from_textfile(path):
    nlp = spacy.load("en_core_web_md")
    classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=7)
    json_lines = []

    logger.info(f"Cleaning file: {path}")
    with open(path, "r", encoding="utf-8") as f:
        texte = f.read()
    doc = nlp(texte)
    phrases = [sent.text.strip() for sent in doc.sents]
    logger.info(f"{len(phrases)} phrases found")

    logger.info(f"Detecting emotions")
    for phrase in phrases:
        phrase = phrase.strip()
        if not phrase:
            continue

        results = classifier(phrase)[0]
        json_line = {
            "emotions": [{"label": res["label"], "score": res["score"]} for res in results]
        }
        json_lines.append(json_line)
    
    logger.info(f"Writing output.json")
    with open(f"txt/output.json", "w", encoding="utf-8") as outfile:     
        json.dump(json_lines, outfile, ensure_ascii=False, indent=2)

    logger.info(f"Done")
    pass



def generate_summary(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def generate_sentences(text):
    generator = pipeline("text2text-generation", model="t5-base")
    prompt = "Extract 3 wise sentences: " + text
    sentences = generator(prompt, max_length=100)[0]["generated_text"]
    return sentences

def generate_heatmap():
    pass






def txt2emo(path=f"txt/input.txt"):

    nlp = spacy.load("en_core_web_md")
    classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=7)
    json_lines = []

    logging.info(f"Processing file: {path}")
    with open(path, "r", encoding="utf-8") as f:
        texte = f.read()
    doc = nlp(texte)
    phrases = [sent.text.strip() for sent in doc.sents]
    logging.info(f"Found {len(phrases)} phrases")

    logging.info(f"Processing phrases")
    for phrase in phrases:
        phrase = phrase.strip()
        if not phrase:
            continue

        results = classifier(phrase)[0]
        json_line = {
            "emotions": [{"label": res["label"], "score": res["score"]} for res in results]
        }
        json_lines.append(json_line)
    
    logging.info(f"Writing output.json")
    with open(f"txt/output.json", "w", encoding="utf-8") as outfile:     
        json.dump(json_lines, outfile, ensure_ascii=False, indent=2)

    logging.info(f"Done")

def process_data_json(data):
    rows = []
    for i, entry in enumerate(data):
        text = entry["text"]
        for emo in entry["emotions"]:
            rows.append({
                "index": i,
                "text": text,
                "emotion": emo["label"],
                "score": emo["score"]
            })
    df = pd.DataFrame(rows)
    return df

def analyze_emotions(df):
    pivot = df.pivot(index="index", columns="emotion", values="score").fillna(0)
    pivot["dominant"] = pivot.idxmax(axis=1)
    return pivot

def interpolate_color(color_hex, score, pale_factor=0.8):
    color_rgb = np.array(mcolors.to_rgb(color_hex))
    white_rgb = np.array([1, 1, 1])
    pale_rgb = white_rgb * pale_factor + color_rgb * (1 - pale_factor)
    result_rgb = pale_rgb * (1 - score) + color_rgb * score
    return result_rgb

def save_heatmap(df, output_path):
    if "dominant" in df.columns:
        data = df.drop(columns="dominant")
    else:
        data = df
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
    plt.imsave(output_path, img)
    logging.info(f"Heatmap saved")

def emotions2shader(path="txt/output.json", output_path="heatmap.png"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    df_long = process_data_json(data)
    df_wide = analyze_emotions(df_long)
    save_heatmap(df_wide, output_path)


if __name__ == "__main__":
    txt2emo ()
    emotions2shader()


