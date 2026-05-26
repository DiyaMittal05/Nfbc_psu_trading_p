"""Load and use the trained sentiment classifier."""

import joblib
from pathlib import Path
from src.config.settings import LOCAL_DATA


class TrainedSentiment:
    """Wrapper around the trained TF-IDF + LogisticRegression classifier."""

    def __init__(self, model_path: str | Path | None = None):
        path = Path(model_path) if model_path else LOCAL_DATA / "models" / "sentiment_clf.joblib"
        if not path.exists():
            raise FileNotFoundError(
                f"Trained model not found at {path}. "
                "Run: uv run python -m src.models.sentiment_trainer"
            )
        self._pipeline = joblib.load(path)

    def predict(self, headline: str) -> tuple[int, float]:
        """
        Predict sentiment direction and confidence.

        Returns:
            (direction, confidence) where direction is +1/-1/0
        """
        label = self._pipeline.predict([headline])[0]
        proba = self._pipeline.predict_proba([headline])[0]

        # Map label to direction
        direction_map = {"positive": 1, "negative": -1, "neutral": 0}
        direction = direction_map.get(label, 0)

        # Confidence = probability of predicted class
        class_index = list(self._pipeline.classes_).index(label)
        confidence = float(proba[class_index])

        return direction, confidence
