import datetime
import os
from bs4 import BeautifulSoup
import urllib.request

import dateparser


def get_page(urlpage, cookie):
  hdr = {
  'cookie': cookie,
  'referer': 'https://moncampus.groupe-igs.fr/'
  }
  req = urllib.request.Request(url = urlpage, headers=hdr)
  page = urllib.request.urlopen(req)
  return BeautifulSoup(page, 'html.parser')

def get_all_data_for_week(page):
  all_day_of_weeks = page.find_all('td',attrs={'class': 'TCJour'})
  all_course = page.find_all('td',attrs={'class': 'TCProf'})
  all_course_code = page.find_all('td',attrs={'class': 'TCase', 'colspan': 2})
  all_hour = page.find_all('td',attrs={'class': 'TChdeb'})
  all_salle = page.find_all('td',attrs={'class': 'TCSalle'})
  return all_day_of_weeks, all_course, all_course_code, all_hour, all_salle

def format_salle(salle):
  try:
    salle = salle[salle.index(':') + 1:]
  except Exception:
    pass
  else:
    return salle

def format_hours(hours):
  try:
    hour_start = hours[:hours.index('-') - 1]
    hour_end = hours[hours.index('-') + 2:]
  except Exception:
    pass
  else:
    return hour_start, hour_end

def format_course(course):
  try:
    course_prof = course[course.index('</span>') + 7:course.index('<br/>')]
    course_name = course[course.index('<br/>')+ 5:]
  except Exception:
    pass
  else:
    return course_prof, course_name

def format_date(day):
  return dateparser.parse(day)

def main(until_month, until_year):
  """
  Get data from the web page and format all data.
  You'll get an array with many elements are formated like this :
  ```python
  {
    'day': datetime.date(2022, 10, 25), 
    'hour': ('13:00 ', '16:30'), 
    'course': ('Teacher name', 'Approfondissement Python (développeurs)'), 
    'course_code': 'IPYT310', 
    'salle': 'B108-S(Bâtiment B)'
  }
  ```
  """
  # Load pages
  format_datas = []
  url = os.environ['URL']
  date_string = url[url.index('&date=') + 6:url.index('&hashURL')] # Get date of URL
  date_parse :datetime.datetime = dateparser.parse(date_string)  # type: ignore

  while date_parse.year != until_year or date_parse.month != until_month:
    page = get_page(url, os.environ['COOKIE'])
    datas = get_all_data_for_week(page)

    # Change date of the url to get next week
    date_string = url[url.index('&date=') + 6:url.index('&hashURL')] # Get date of URL
    print(f'Actually scrapped : {date_string}')
    date_parse :datetime.datetime = dateparser.parse(date_string)  # type: ignore
    date_parse += datetime.timedelta(days=7) # type: ignore

    # Check to add a 0 to the day or the month
    month = date_parse.month if date_parse.month > 9 else f'0{date_parse.month}'
    day = date_parse.day if date_parse.day > 9 else f'0{date_parse.day}'
    url = url.replace(date_string, f'{month}/{day}/{date_parse.year}')

    # Get table of each array and get ONLY 5 days of the week and 10 first elements for others arrays
    all_day_of_weeks = datas[0][5:10]
    all_hour = datas[3][0:10]
    all_course = datas[1][0:10]
    all_course_code = datas[2][0:10]
    all_salle = datas[4][0:10]
    for i in range(10):
      try:
        hours = format_hours(all_hour[i].text)
        actual_day = all_day_of_weeks[i//2].text
        format_datas.append({
          'day_start': format_date(f'{actual_day} {date_parse.year} {hours[0]}'), # type: ignore
          'day_end': format_date(f'{actual_day} {date_parse.year} {hours[1]}'), # type: ignore 
          'course': format_course(all_course[i].renderContents().decode('utf-8')), 
          'course_code': all_course_code[i].text, 
          'salle': format_salle(all_salle[i].text)
          })
      except:
        continue

  return format_datas