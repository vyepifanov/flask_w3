import json


def add_booking(id, day, time, name, phone):
    try:
        with open('./db/booking.json', 'r') as r:
            records = json.load(r)
    except IOError:
        records = []

    records.append({"id":id, "day":day, "time":time, "name":name, "phone":phone})
    with open('./db/booking.json', 'w') as w:
        w.write(json.dumps(records))


def add_request(goal, hour, name, phone):
    try:
        with open('./db/request.json', 'r') as r:
            records = json.load(r)
    except IOError:
        records = []

    records.append({"goal":goal, "hour":hour, "name":name, "phone":phone})
    with open('./db/request.json', 'w') as w:
        w.write(json.dumps(records))
