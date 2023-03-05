import datetime
import json
import calendar
import random
event_distribution_old = [0,0,0,0,1,2,5,9,10,10,7,8,7,7,7,7,4,2,1,0,0,0,0,0]
event_distribution = [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0]
benign_template = json.load(open('./bases/benign_template.json'))
malicious_template = json.load(open('./bases/malicious_template.json'))


day_base = {
    "date": "",
    "day_of_week" : "",
    "number_of_events" : "",
    "events" : [

    ]
}

def get_event(event_type,time):
    # get random event from pool
    if(event_type =='benign'):
        event = random.choice(benign_template).copy()
    else:
        event = random.choice(malicious_template).copy() 

    # fix timstamps
    between = [time, (time + datetime.timedelta(hours=1))]
    random_time_in_interval = random.randint(between[0].timestamp(),between[1].timestamp())
    event['clock'] = [str(datetime.datetime.fromtimestamp(random_time_in_interval)),int(datetime.datetime.fromtimestamp(random_time_in_interval).timestamp())]

    # get which option to execute for each option type
    selected_options = [None] * len(event['options'])
    for option in range(0,len(event['options'])):
        selected_options[option] = random.choice(event['options'][option])
    event['options'] = selected_options
    return event

def save_timeline(timeline):
    #Serialize and save timeline
    json_object = json.dumps(timeline, indent=2, sort_keys=True, default=str)
    with open('timeline.json','w') as outfile:
        outfile.write(json_object)

def gen_timeline(start,end):
    start_time = datetime.datetime.strptime(start, "%d/%m/%Y")
    stop_time = datetime.datetime.strptime(end, "%d/%m/%Y")
    number_of_days= (stop_time-start_time).days
    timeline = [None] * number_of_days

    # Generate base for timeline
    for n in range(0,number_of_days):
        current_date = start_time.date() + datetime.timedelta(days=n)
        day = day_base.copy()
        day['date'] = current_date
        day['day_of_week'] = [current_date.weekday(),calendar.day_name[current_date.weekday()]]
        if day['day_of_week'][0] in range(0,4):
            # for each hour in WEEKDAYS
            for hour in range(0,23):
                #get number of interactions for that hour
                hourly_interactions = event_distribution_old[hour]
                
                #for all interactions
                for i in range (0,hourly_interactions):
                    tmp_event = get_event('benign',start_time + datetime.timedelta(days=n,hours=hour))
                    print(tmp_event['clock'])
                    day['events'].append(tmp_event)
                # sort the events
                day['events'] = sorted(day['events'],key=lambda x: x['clock'][1])

            day['number_of_events'] = len(day['events'])
        timeline[n] = day

    #Serialize and save timeline to file
    save_timeline(timeline)
    #print(json.dumps(timeline, indent=2, sort_keys=True, default=str))

 
gen_timeline('01/01/2022', '01/02/2022')