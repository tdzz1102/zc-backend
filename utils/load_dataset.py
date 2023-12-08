import pandas as pd
import re
from requests import Session
from pathlib import Path
from db import dataset_exists


def get_session():
    s = Session()
    s.trust_env = False
    try:
        yield s
    finally:
        s.close()


def load_select_dataset(dataset_path: Path):
    if dataset_exists(dataset_path.stem):
        print(f"Dataset {dataset_path.stem} already exists")
        return
    
    s = next(get_session())
    # create dataset
    res = s.post('http://localhost:8000/dataset', json={'name': dataset_path.stem})
    dataset_id = res.json()['id']
    
    # create data
    df = pd.read_csv(dataset_path).dropna()
    
    def create_data_from_line(line: pd.DataFrame):
        d = line.drop(['id'], errors='ignore').to_dict()
        # A, B, C, D -> 0, 1, 2, 3
        print(d['answer'])
        d['answer'] = ord(d['answer']) - ord('A')
        res = s.post('http://localhost:8000/data', json={**d, 'dataset_id': dataset_id, 'type': 'select'})
        return res
    
    df.apply(create_data_from_line, axis=1)
    

def load_mmlu_select_dataset(dataset_path: Path):
    if dataset_exists(dataset_path.stem):
        print(f"Dataset {dataset_path.stem} already exists")
        return
    
    s = next(get_session())
    # create dataset
    res = s.post('http://localhost:8000/dataset', json={'name': dataset_path.stem})
    dataset_id = res.json()['id']
    
    # create data
    df = pd.read_csv(dataset_path).dropna()
    
    def create_data_from_line(line: pd.DataFrame):
        d = line.to_dict()
        pattern = r'"([^"]+)"'
        matches = re.findall(pattern, d['choices'])
        options = [match for match in matches if not match.startswith(',')]
        d['A'] = options[0]
        d['B'] = options[1]
        d['C'] = options[2]
        d['D'] = options[3]
        d['answer'] = int(d['answer'][0])
        res = s.post('http://localhost:8000/data', json={**d, 'dataset_id': dataset_id, 'type': 'select'})
        return res
    
    df.apply(create_data_from_line, axis=1)


def load_qa_dataset(dataset_path: Path):
    if dataset_exists(dataset_path.stem):
        print(f"Dataset {dataset_path.stem} already exists")
        return
    
    s = next(get_session())
    # create dataset
    res = s.post('http://localhost:8000/dataset', json={'name': dataset_path.stem})
    dataset_id = res.json()['id']
    
    # create data
    df = pd.read_csv(dataset_path, names=['question', 'subject', 'answer', 'answer_GPT35', 'answer_GPT4']).dropna()
    
    def create_data_from_line(line: pd.DataFrame):
        d = line.to_dict()
        res = s.post('http://localhost:8000/data', json={**d, 'dataset_id': dataset_id, 'type': 'qa'})
        return res
    
    df.apply(create_data_from_line, axis=1)
    

def load_all_dataset():
    data_path = Path(__file__).parent.parent / "data"
    load_select_dataset(data_path / "ceval_select.csv")
    load_select_dataset(data_path / "cmmlu_select.csv")
    load_mmlu_select_dataset(data_path / "mmlu_select.csv")
    load_qa_dataset(data_path / "zbench_common.csv")
    load_qa_dataset(data_path / "zbench_emergent.csv")
    

if __name__ == "__main__":
    load_all_dataset()
