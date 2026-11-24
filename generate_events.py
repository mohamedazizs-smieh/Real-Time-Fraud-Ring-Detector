from datetime import datetime,timedelta
def random_timestamp(time_range,rng):
    start=time_range['start']
    end=time_range['end']
    if isinstance(start, str):
        start = datetime.fromisoformat(start)
    if isinstance(end, str):
        end = datetime.fromisoformat(end)
    delta=end-start
    rng_seconds=rng.randint(0,int(delta.total_seconds()))
    return start+timedelta(seconds=rng_seconds)
    


def generate_normal_events(configs,rng):
    events=list()
    for i in range(configs['normal_events']['count']):
        user_id=rng.randint(*configs['normal_events']['user_id_range'])
        product_id=rng.randint(*configs['normal_events']['product_id_range'])
        rating=rng.choices(list(configs['normal_events']['rating_distribution'].keys()),
                              list(configs['normal_events']['rating_distribution'].values()))[0]
        timestamp=random_timestamp(configs['normal_events']['timestamp_range'],rng)
        events.append({
            'ring_id':None,
            'user_id':user_id,
            'product_id':product_id,
            'rating':rating,
            'timestamp':timestamp.isoformat(),
            'is_fraud': False
        })
    return events

def generate_fraud_events(configs,rng):
    events=list()
    for i in range(configs['fraud_events']['count']):
        timestamp=random_timestamp(configs['fraud_events']['timestamp_range'],rng)
        user_id=rng.randint(*configs['fraud_events']['fraud_user_ids'])
        case=rng.choices(['boost', 'nerf'],
        weights=[
            configs['fraud_events']['attackers_strategies']['allies_boost']['weight'],
            configs['fraud_events']['attackers_strategies']['competitors_nerf']['weight']
            ])[0]
        if case=='boost':
            rating=configs['fraud_events']['attackers_strategies']['allies_boost']['rating_product']
            product_id=configs['fraud_events']['attackers_strategies']['allies_boost']['target_product'][0]
        else:
            rating=configs['fraud_events']['attackers_strategies']['competitors_nerf']['rating_product']
            product_id=configs['fraud_events']['attackers_strategies']['competitors_nerf']['target_product'][0]
        events.append(
            {
            'ring_id':0,
            'user_id':user_id,
            'product_id':product_id,
            'rating':rating,
            'timestamp':timestamp.isoformat(), 
            'is_fraud': True
            }
        )
    return events

