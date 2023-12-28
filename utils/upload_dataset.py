import pandas as pd
from pathlib import Path
from utils.db import get_db
from schema.data import DataType, QAData, SelectData
from schema.dataset import Dataset
from utils.logging import logger
from fastapi.encoders import jsonable_encoder


def upload_data_to_dataset(dataset_id: str, file_path: str):
    db = next(get_db())
    dataset_key = f"dataset:{dataset_id}"

    if not db.exists(dataset_key):
        logger.error(f"Dataset with ID {dataset_id} does not exist.")
        return

    dataset_info = db.hgetall(dataset_key)
    dataset_type = dataset_info.get('type', DataType.select)

    data_path = Path(file_path)
    if not data_path.exists() or not data_path.is_file():
        logger.error(f"File not found: {file_path}")
        return

    df = pd.read_csv(data_path)
    for _, row in df.iterrows():
        data_dict = row.to_dict()
        if dataset_type == DataType.select:
            data_instance = SelectData(
                **data_dict, dataset_id=dataset_id, type=DataType.select
            )
        else:
            data_instance = QAData(**data_dict, dataset_id=dataset_id, type=DataType.qa)

        db.hmset(
            f"data:{data_instance.id}",
            jsonable_encoder(data_instance, exclude_none=True),
        )

    logger.info(f"Data from {file_path} uploaded successfully to dataset {dataset_id}")


# upload_data_to_dataset("dataset_id", "path")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python upload_data.py [dataset_id]")
        sys.exit(1)

    dataset_id = sys.argv[1]
    file_path = Path(__file__).parent.parent / "data" / sys.argv[2]
    upload_data_to_dataset(dataset_id, file_path)
