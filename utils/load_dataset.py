import pandas as pd
import numpy as np
import re
from pathlib import Path
from schema.data import SelectData, QAData, DataType
from fastapi.encoders import jsonable_encoder
from schema.dataset import Dataset
from utils.db import dataset_exists, get_db
from utils.logging import logger


def load_select_dataset(dataset_path: Path, mmlu=False):
    if dataset_exists(dataset_path.stem):
        logger.info(f"Dataset {dataset_path.stem} already exists")
        return
    
    # create dataset
    r = next(get_db())
    dataset = Dataset(name=dataset_path.stem)
    r.hmset(f"dataset:{dataset.id}", jsonable_encoder(dataset, exclude_none=True))

    # create data
    df = pd.read_csv(dataset_path).dropna()
    
    def create_data_from_line(line: pd.DataFrame):
        d = line.drop(['id'], errors='ignore').to_dict()
        d['answer'] = ord(d['answer']) - ord('A')
        select_data = SelectData(**d, dataset_id=dataset.id, type=DataType.select)
        r.hmset(f"data:{select_data.id}", jsonable_encoder(select_data, exclude_none=True))
        r.sadd('autorating', str(select_data.id))
        return select_data
    
    def create_mmlu_data_from_line(line: pd.DataFrame):
        d = line.to_dict()
        pattern = r'"([^"]+)"'
        matches = re.findall(pattern, d['choices'])
        options = [match for match in matches if not match.startswith(',')]
        d['A'] = options[0]
        d['B'] = options[1]
        d['C'] = options[2]
        d['D'] = options[3]
        d['answer'] = int(d['answer'][0])
        select_data = SelectData(**d, dataset_id=dataset.id, type=DataType.select)
        r.hmset(f"data:{select_data.id}", jsonable_encoder(select_data, exclude_none=True))
        r.sadd('autorating', str(select_data.id))
        return select_data
    
    df.apply(create_data_from_line if not mmlu else create_mmlu_data_from_line, axis=1)
    

def load_qa_dataset(dataset_path: Path):
    if dataset_exists(dataset_path.stem):
        logger.info(f"Data·set {dataset_path.stem} already exists")
        return
    
    # create dataset
    r = next(get_db())
    dataset = Dataset(name=dataset_path.stem)
    r.hmset(f"dataset:{dataset.id}", jsonable_encoder(dataset, exclude_none=True))
    
    # create data
    df = pd.read_csv(dataset_path, names=['question', 'subject', 'answer', 'answer_GPT35', 'answer_GPT4'])
    df.replace([np.nan], [None], inplace=True)
    
    def create_data_from_line(line: pd.DataFrame):
        d = line.to_dict()
        qa_data = QAData(**d, dataset_id=dataset.id, type=DataType.qa)
        r.hmset(f"data:{qa_data.id}", jsonable_encoder(qa_data, exclude_none=True))
        return qa_data
    
    df.apply(create_data_from_line, axis=1)
    

def load_all_dataset():
    data_path = Path(__file__).parent.parent / "data"
    load_select_dataset(data_path / "ceval_select.csv")
    load_select_dataset(data_path / "cmmlu_select.csv")
    load_select_dataset(data_path / "mmlu_select.csv", mmlu=True)
    load_qa_dataset(data_path / "zbench_common.csv")
    load_qa_dataset(data_path / "zbench_emergent.csv")
    

if __name__ == "__main__":
    load_all_dataset()
