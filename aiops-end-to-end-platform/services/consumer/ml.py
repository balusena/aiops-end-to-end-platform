from sklearn.ensemble import IsolationForest

models = {}
history = {}

WARMUP = 30
MAX_HISTORY = 200


def predict(service, features):
    X = [
        features["cpu"],
        features["memory"],
        features["error_rate"],
        features["latency"]
    ]

    if service not in history:
        history[service] = []

    history[service].append(X)

    # keep memory bounded
    if len(history[service]) > MAX_HISTORY:
        history[service].pop(0)

    if len(history[service]) < WARMUP:
        return 1

    if service not in models:
        model = IsolationForest(contamination=0.05)
        model.fit(history[service])
        models[service] = model
        return 1

    return models[service].predict([X])[0]