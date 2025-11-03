import json


def export_dataset(dataset: dict, out_path: str):
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    return out_path
