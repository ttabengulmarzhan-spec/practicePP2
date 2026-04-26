import json
import os


SETTINGS_DEFAULT = {
    "sound": True,
    "difficulty": "normal",   # easy | normal | hard
    "car_color": "blue"        # red | blue | green | yellow
}


def _read_json(path, default_value):
    if not os.path.exists(path):
        return default_value
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default_value


def _write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_settings(path="settings.json"):
    data = _read_json(path, {})
    settings = dict(SETTINGS_DEFAULT)
    settings.update(data if isinstance(data, dict) else {})
    return settings


def save_settings(settings, path="settings.json"):
    _write_json(path, settings)


def load_leaderboard(path="leaderboard.json"):
    data = _read_json(path, [])
    if not isinstance(data, list):
        return []
    return sorted(data, key=lambda x: x.get("score", 0), reverse=True)[:10]


def add_score(entry, path="leaderboard.json"):
    board = load_leaderboard(path)
    board.append(entry)
    board = sorted(board, key=lambda x: x.get("score", 0), reverse=True)[:10]
    _write_json(path, board)
    return board

