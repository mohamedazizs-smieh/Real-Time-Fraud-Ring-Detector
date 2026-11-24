import yaml,os,json,random
from generate_events import generate_normal_events, generate_fraud_events
def build_events(configs):
    rng = random.Random(configs['random_seed'])
    normal_events = generate_normal_events(configs,rng)
    fraud_events = generate_fraud_events(configs,rng)
    events=sorted(normal_events+fraud_events,key=lambda e: (e['timestamp'], e['user_id'], e['product_id']),)
    return events
def main():
    with open("configs.yaml") as config_f:
        configs=yaml.safe_load(config_f)
    directory = configs['output_folder'] 
    try:
        os.makedirs(directory, exist_ok=True)
        print("Directory '%s' created successfully" % directory)
    except OSError as error:
        print("Directory can not be created")
    path_data = os.path.join(directory, "data.jsonl")
    events=build_events(configs)
    with open(path_data, mode="w", encoding="utf-8") as write_file:
        
        for i in events:
            write_file.write(json.dumps(i)+"\n")
if __name__ == "__main__":
    main()