
import os
import pickle
import torch

from cnn_intent import CNNIntentClassifier

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VOCAB_PATH = os.path.join(BASE_DIR, "data", "vocab.pkl")
MODEL_PATH = os.path.join(BASE_DIR, "models", "cnn_best.pt")

LABELS = {
    0: "friendly",
    1: "hostile",
    2: "trade",
    3: "quest",
}

MAX_LEN = 64
EMBED_DIM = 50
HIDDEN_DIM = 64
FILTER_SIZES = [2, 3, 4]

device = torch.device("cpu")

# Load the vocabulary created by train_intent.py
with open(VOCAB_PATH, "rb") as file:
    vocab = pickle.load(file)

# Build the CNN using the same architecture as training.
model = CNNIntentClassifier(
    len(vocab),
    EMBED_DIM,
    HIDDEN_DIM,
    FILTER_SIZES,
    len(LABELS),
    MAX_LEN,
)

# Load trained weights.
state_dict = torch.load(
    MODEL_PATH,
    map_location=device,
    weights_only=True,
)
model.load_state_dict(state_dict)
model.to(device)
model.eval()


def classify_intent(text):
    """Classify a player's message using the trained CNN."""
    if not isinstance(text, str) or not text.strip():
        return {"intent": "friendly", "confidence": 0.0}

    tokens = [
        vocab.get(char, vocab["<UNK>"])
        for char in text.lower()
    ]

    tokens = tokens[:MAX_LEN]
    tokens += [vocab["<PAD>"]] * (MAX_LEN - len(tokens))

    inputs = torch.tensor([tokens], dtype=torch.long).to(device)

    with torch.no_grad():
        outputs = model(inputs)
        probabilities = torch.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, dim=1)

    return {
        "intent": LABELS[predicted.item()],
        "confidence": round(confidence.item(), 3),
    }
