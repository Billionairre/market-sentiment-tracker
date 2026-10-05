from transformers import pipeline

class SentimentClassifier:
    def __init__(self):
        # Lightweight model for CPU inference
        model_path = "cardiffnlp/twitter-roberta-base-sentiment-latest"
        self.pipe = pipeline(
            "text-classification",
            model=model_path,
            tokenizer=model_path,
            top_k=None,
            device=-1  # Uses CPU
        )

    def analyze(self, text):
        if not text or not text.strip():
            return {"label": "Neutral", "score": 0.0}

        predictions = self.pipe(text)[0]
        
        # Sort predictions by highest confidence score
        top_pred = sorted(predictions, key=lambda x: x["score"], reverse=True)[0]
        
        label_raw = top_pred["label"].lower()
        score = float(top_pred["score"])
        
        if "positive" in label_raw:
            label = "Positive"
        elif "negative" in label_raw:
            label = "Negative"
        else:
            label = "Neutral"

        return {"label": label, "score": round(score, 4)}

# Singleton pattern to prevent reloading model on every request
classifier_instance = None

def get_classifier():
    global classifier_instance
    if classifier_instance is None:
        classifier_instance = SentimentClassifier()
    return classifier_instance