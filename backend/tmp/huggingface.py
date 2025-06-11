from transformers import pipeline
import numpy as np
from pprint import pprint
import logging

from app.config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


class HuggingFace:
    def __init__(self, model_name="j-hartmann/emotion-english-distilroberta-base", segment_size=1000, is_long=False, long_text_threshold=1000):
        self._model_name = model_name
        self._segment_size = segment_size
        self._is_long = is_long
        self._long_text_threshold = long_text_threshold
        self._classifier = pipeline("text-classification", model=self._model_name, top_k=None)

    @property
    def model_name(self):
        return self._model_name

    @model_name.setter
    def model_name(self, value):
        self._model_name = value
        self._classifier = pipeline("text-classification", model=value, top_k=None)

    @property
    def segment_size(self):
        return self._segment_size

    @segment_size.setter
    def segment_size(self, value):
        self._segment_size = value

    @property
    def is_long(self):
        return self._is_long

    @is_long.setter
    def is_long(self, value):
        self._is_long = value

    @property
    def long_text_threshold(self):
        return self._long_text_threshold

    @long_text_threshold.setter
    def long_text_threshold(self, value):
        self._long_text_threshold = value

    def classify(self, text):
        """
        Classifies text. If text is longer than long_text_threshold, splits and aggregates (long text logic), else single call.
        Returns une liste de dicts [{'label': ..., 'score': ...}] dans tous les cas (format pipeline par défaut).
        """
        try:
            if len(text) <= self._long_text_threshold:
                return self._classifier(text)
            # Long text logic
            logger.info(f"Classifying text: {text[:30]}[...]")
            logger.info(f"Text is longer than {self._long_text_threshold} characters, splitting...")
            segments = [text[i:i+self._segment_size] for i in range(0, len(text), self._segment_size)]
            all_scores = []
            for segment in segments:
                scores = self._classifier(segment)[0]  # [0] car return_all_scores=True
                all_scores.append(scores)
            emotions = [score['label'] for score in all_scores[0]]
            scores_matrix = np.array([[score['score'] for score in segment_scores] for segment_scores in all_scores])
            mean_scores = scores_matrix.mean(axis=0)
            return [
                {'label': label, 'score': float(score)}
                for label, score in zip(emotions, mean_scores)
            ]
        except Exception as e:
            pprint({"error": str(e)})
            return {"error": str(e)}

    def classify_from_file(self, pathfile):
        """
        Lit un fichier texte et applique classify sur son contenu.
        Args:
            pathfile (str): Chemin du fichier texte à analyser.
        Returns:
            dict: Probabilités moyennes par émotion sur l'ensemble du texte (si long), ou pipeline output (si court).
        """
        try:
            with open(pathfile, 'r', encoding='utf-8') as f:
                text = f.read()
            return self.classify(text)
        except Exception as e:
            pprint({"error": str(e)})
            return {"error": str(e)}

# Exemple d'utilisation :
hf = HuggingFace()
result = hf.classify("Votre très long texte ici ...")
pprint(result)

# Exemple d'utilisation avec un fichier texte :
result = hf.classify_from_file("app/utils/text.txt")
pprint(result)


