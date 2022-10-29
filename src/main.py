# argparse for parameters
from scrap import main
from ical import create_ics, create_calendar_and_events

if __name__ == '__main__':
  week = main()
  calendar = create_calendar_and_events(week)
  create_ics(calendar)