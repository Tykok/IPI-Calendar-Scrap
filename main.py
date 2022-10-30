# argparse for parameters
from src.scrap import main
from src.ical import create_ics, create_calendar_and_events
from dotenv import load_dotenv

if __name__ == '__main__':
  load_dotenv()
  print('For month, don\'t wrote 07 for July. Write 7')
  month = int(input('Until (month) :'))
  year = int(input('Until (year) :'))
  week = main(month, year)
  calendar = create_calendar_and_events(week)
  create_ics(calendar)