import redis
import pandas as pd
from pathlib import Path
from utils.db import get_db
from schema.data import DataType

# REDIS_URL=redis://localhost:6379/5


def download_dataset(dataset_id: str, output_dir: Path):
    redis_url = "redis://localhost:6379/5"
    r = redis.Redis.from_url(redis_url, decode_responses=True)
    yield r
    dataset_key = f"dataset:{dataset_id}"
    if not r.exists(dataset_key):
        print(f"Dataset with ID {dataset_id} does not exist")
        return

    data_keys = r.keys(f"data:*")
    data = []

    for key in data_keys:
        data_dict = r.hgetall(key)
        if data_dict.get('dataset_id') == dataset_id:
            data.append(data_dict)

    if not data:
        print(f"No data found for dataset ID {dataset_id}")
        return

    df = pd.DataFrame(data)
    df.to_csv(output_dir / f"{dataset_id}.csv", index=False)

    print(
        f"Dataset {dataset_id} downloaded successfully to {output_dir / f'{dataset_id}.csv'}"
    )


# output_dir = Path(__file__).parent.parent / "data"
# download_dataset("dataset_id", output_dir)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python download_dataset.py [dataset_id]")
        sys.exit(1)

    dataset_id = sys.argv[1]
    output_dir = Path(__file__).parent.parent / "data"
    # output_dir.mkdir(exist_ok=True)
    download_dataset(dataset_id, output_dir)
