import random
from datetime import datetime,timedelta
def random_timestamp(time_range):
    start=time_range['start']
    end=time_range['end']
    if isinstance(start, str):
        start = datetime.fromisoformat(start)
    if isinstance(end, str):
        end = datetime.fromisoformat(end)
    delta=end-start
    random_seconds=random.randint(0,int(delta.total_seconds()))
    return start+timedelta(seconds=random_seconds)
    


def generate_normal_events(configs):
    events=list()
    for i in range(configs['normal_events']['count']):
        user_id=random.randint(*configs['normal_events']['user_id_range'])
        product_id=random.randint(*configs['normal_events']['product_id_range'])
        rating=random.choices(list(configs['normal_events']['rating_distribution'].keys()),
                              list(configs['normal_events']['rating_distribution'].values()))[0]
        timestamp=random_timestamp(configs['normal_events']['timestamp_range'])
        events.append({
            'user_id':user_id,
            'product_id':product_id,
            'rating':rating,
            'timestamp':timestamp.isoformat()
        })
    return events

def generate_fraud_events(configs):
    events=list()
    for i in range(configs['fraud_events']['count']):
        timestamp=random_timestamp(configs['fraud_events']['timestamp_range'])
        user_id=random.randint(*configs['fraud_events']['fraud_user_ids'])
        case=random.choices([0,1],[configs['fraud_events']['attackers_strategies']['allies_boost']['weight'],
                configs['fraud_events']['attackers_strategies']['competitors_nerf']['weight']])[0]
        if case==1:
            rating=configs['fraud_events']['attackers_strategies']['allies_boost']['rating_product']
            product_id=configs['fraud_events']['attackers_strategies']['allies_boost']['target_product'][0]
        else:
            rating=configs['fraud_events']['attackers_strategies']['competitors_nerf']['rating_product']
            product_id=configs['fraud_events']['attackers_strategies']['competitors_nerf']['target_product'][0]
        events.append(
            {
            'user_id':user_id,
            'product_id':product_id,
            'rating':rating,
            'timestamp':timestamp.isoformat(), 
            'is_fraud': True
            }
        )
    return events

def hide(normal_events,fraud_events):
    all_events=normal_events+fraud_events
    random.shuffle(all_events)
    return all_events