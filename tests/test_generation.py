import pytest
import yaml,sys,subprocess,shutil
from pathlib import Path
from datetime import datetime
from main import build_events
@pytest.fixture(scope="module")
def configs():
    with open("configs.yaml") as config_f:
        configs=yaml.safe_load(config_f)
        return configs

@pytest.fixture(scope="module")
def events(configs):
    return build_events(configs)

def test_generation(configs,events):
    
    assert(configs['fraud_events']['count'] == len([e for e in events if e['is_fraud']]))
    assert(configs['normal_events']['count'] == len([e for e in events if not e['is_fraud']]))

def test_parse(configs,events):
    start_f=datetime.fromisoformat(configs['fraud_events']['timestamp_range']['start'])
    end_f=datetime.fromisoformat(configs['fraud_events']['timestamp_range']['end'])
    start_n=datetime.fromisoformat(configs['normal_events']['timestamp_range']['start'])
    end_n=datetime.fromisoformat(configs['normal_events']['timestamp_range']['end'])
    for e in events:
        if e['is_fraud']:
            assert(start_f<= datetime.fromisoformat(e['timestamp'])<=end_f)
        else:  
            assert(start_n<= datetime.fromisoformat(e['timestamp'])<=end_n)


def test_sorted_order(events):

    assert(sorted(events,key=lambda e: (e['timestamp'], e['user_id'], e['product_id']),) == events)

def test_ring_ids(events):
    assert(all([e['ring_id'] ==0 for e in events if e['is_fraud']]  ))
    assert(all([e['ring_id'] is None for e in events if not e['is_fraud']]  ))

def test_path(tmp_path):
  source = Path("configs.yaml")
  dest = tmp_path / "configs.yaml"
  shutil.copy(source, dest)
  script_path = Path(__file__).resolve().parents[1] / "main.py"
    
  subprocess.run([sys.executable, str(script_path)],cwd=tmp_path,check=True,)
  first = (tmp_path / "output" / "data.jsonl").read_bytes()
  subprocess.run([sys.executable, str(script_path)],cwd=tmp_path,check=True,)
  second = (tmp_path / "output" / "data.jsonl").read_bytes()
  assert(first == second)