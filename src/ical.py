from ics import Event, Calendar
from datetime import datetime
from pytz import timezone

def create_events(calendar: Calendar, date_start: datetime, date_end: datetime, name: str, description: str):
  # local = datetime.now()
  # utc = datetime.utcnow()
  # time_diff = int((local - utc).days * 86400 + round((local - utc).seconds, -1))

  e = Event()
  e.name = name
  e.description = description
  e.begin = date_start.astimezone(timezone('Europe/Paris'))
  e.end = date_end.astimezone(timezone('Europe/Paris'))
  calendar.events.add(e)
  print(calendar.events)
  return calendar

def create_calendar_and_events(datas):
  calendar = Calendar()
  for i in datas:
    description = f"""
    Intervenant : {i['course'][0]}
    Code : {i['course_code']}
    Salle : {i['salle']}
    """
    calendar = create_events(calendar, i['day_start'], i['day_end'], i['course'][1], description)
  return datas

def create_ics(calendar):
  with open('/home/tykok/Projet/IPI-Calendar-Scrap/my.ics', 'w') as f:
    f.writelines(calendar.serialize_iter())