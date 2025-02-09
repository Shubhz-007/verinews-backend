# credibility.py
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import requests

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")


def analyze_credibility(text):
    # Clickbait detection
    clickbait_terms = ["shocking", "miracle", "you won't believe"]
    clickbait_score = sum(1 for term in clickbait_terms if term in text.lower())

    # Extract entities (people, orgs, locations)
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents if ent.label_ in ["PERSON", "ORG", "GPE"]]

    # Cross-reference with Wikipedia
    wiki_matches = 0
    for entity in entities[:3]:  # Limit to 3 entities to avoid API overuse
        response = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "list": "search",
                "srsearch": entity,
                "format": "json",
            },
        )
        if response.json()["query"]["search"]:
            wiki_matches += 1

    # Calculate score
    score = 50 + (wiki_matches * 15) - (clickbait_score * 10)
    score = max(0, min(100, score))  # Ensure score is between 0-100

    # Generate flags
    flags = []
    if clickbait_score > 2:
        flags.append("clickbait-language")
    if wiki_matches < 1:
        flags.append("unverified-entities")

    print(
        f"Wiki matches: {wiki_matches}, Clickbait score: {clickbait_score}, Raw score: {score}"
    )

    return score, flags
