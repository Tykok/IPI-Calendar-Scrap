from icalendar import Event

def create_events(calendar, date_start, date_end, name, description):
  e = Event()
  # Update with icalendar instead of ics
  e.name = name
  e.description = description
  e.begin = date_start
  e.end = date_end
  calendar.events.add(e)

  return calendar

def create_ics(calendar):
  with open('/home/tykok/Projet/IPI-Calendar-Scrap/my.ics', 'w') as f:
    f.writelines(calendar.serialize_iter())