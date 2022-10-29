# argparse for parameters
from ics import Calendar
from scrap import main
from ical import create_events, create_ics
import os

os.environ['TZ'] = 'Europe/Paris'
if __name__ == '__main__':
  week = main()
  calendar = Calendar()
  for i in week:
    description = f"""
    Intervenant : {i['course'][0]}
    Code : {i['course_code']}
    Salle : {i['salle']}
    """
    # start = f"{i['day']} {i['hour'][0]}:00"
    # end = f"{i['day']} {i['hour'][1]}:00"
    calendar = create_events(calendar, i['day_start'], i['day_end'], i['course'][1], description)
  create_ics(calendar)