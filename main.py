import yaml,os,json,random
from generate_events import generate_normal_events, generate_fraud_events, hide
def main():
    with open("configs.yaml") as config_f:
        configs=yaml.safe_load(config_f)
    random.seed(configs['random_seed'])
    normal_events = generate_normal_events(configs)
    fraud_events = generate_fraud_events(configs)
    events = hide(normal_events,fraud_events)
    directory = configs['output_folder'] 
    try:
        os.makedirs(directory, exist_ok=True)
        print("Directory '%s' created successfully" % directory)
    except OSError as error:
        print("Directory can not be created")
    path_data = os.path.join(directory, "data.jsonl")
    with open(path_data, mode="w", encoding="utf-8") as write_file:
        
        for i in events:
            write_file.write(json.dumps(i)+"\n")
if __name__ == "__main__":
    main()