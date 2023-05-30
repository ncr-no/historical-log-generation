import datetime
import json
import calendar
import random
import os
event_distribution_normal = [0,0,0,0,0,2,4,8,9,10,10,10,10,9,5,3,3,2,1,0,0,0,0,0]
event_distribution_247 = [4,4,4,5,4,5,5,8,9,10,10,10,10,9,7,6,5,4,4,4,4,4,4,4]

script_dir = os.path.dirname(__file__)
benign_template = json.load(open(os.path.join(script_dir, 'bases\\benign_template.json')))
malicious_template = json.load(open(os.path.join(script_dir, 'bases\\malicious_template.json')))

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

def gen_timeline(start,end,schedule):
    print('> Generating timeline')
    print('>',start,end,schedule)
    start_time = datetime.datetime.strptime(start, "%d/%m/%Y")
    stop_time = datetime.datetime.strptime(end, "%d/%m/%Y")
    number_of_days= (stop_time-start_time).days
    if number_of_days == 0:
        number_of_days = 1
    timeline = [None] * number_of_days

    # Generate base for timeline

    # For each day generate the events
    for n in range(0,number_of_days):
        current_date = start_time.date() + datetime.timedelta(days=n)
        day = day_base.copy()
        day['date'] = current_date
        day['day_of_week'] = [current_date.weekday(),calendar.day_name[current_date.weekday()]]
        # For each day, based on 5 or 7 day schedule
        if day['day_of_week'][0] in range(5 if schedule=='normal' else 7):
            # Generate benign events for each hour in schedule
            for hour in range(0,23):
                #get number of interactions for that hour
                if(schedule == 'normal'):
                    hourly_interactions = event_distribution_normal[hour]
                else:
                    hourly_interactions = event_distribution_247[hour]
                    
                #for all interactions
                for i in range (0,hourly_interactions):
                    tmp_event = get_event('benign',start_time + datetime.timedelta(days=n,hours=hour))
                    day['events'].append(tmp_event)
                    # Sort the events
                day['events'] = sorted(day['events'],key=lambda x: x['clock'][1])

            # Generate malicious events if any
            if(random.randint(0,100) < 50):
                # Generating malicious event
                tmp_event = get_event('malicious',start_time + datetime.timedelta(days=n,hours=random.choice([21,22,23,1,2,3,4])))
                day['events'].append(tmp_event)
                day['events'] = sorted(day['events'],key=lambda x: x['clock'][1])

            # Add number of events to day
            day['number_of_events'] = len(day['events'])
        timeline[n] = day

    #Serialize and save timeline to file
    try:
      save_timeline(timeline)
      print('> Timeline generated successfully')
      return True
    except:
      return False

