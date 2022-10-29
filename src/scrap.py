from array import array
from datetime import date
from bs4 import BeautifulSoup
import urllib.request

import dateparser


def get_page(cookie):
  urlpage = 'https://ws-edt-igs.wigorservices.net//WebPsDyn.aspx?action=posEDTLMS&serverID=G&Tel=elie.treport&date=10/29/2022&hashURL=18864BCBD471E0FD124E751E55AA00F72C6BC3FF32FB74D68FE69495251392A8901E18BB955F215583E9EBCD018358C5D0BEBC52D4E44CC2BCF2D2345122DD17'
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

def main():
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
  page = get_page('ASP.NET_SessionId=swichxnkim2iroomp3uhbfez; .DotNetCasClientAuth=C8A00B242B116BD0536D3DAAB024EBB6F04B439424565CB71F231922A177AD624A5F9C37E8CE6D1406F7A21D66BAF951812A6C92D1185AAAF368D6B1BDF4B4842E0909FAB9B15FEE2642EBF8BDC8FB48383C70CE8F3B42D6055232DEAD9480AD0ED4C94B0FBE6339E0720C3C5C87240E731841F63C5F87F4271797C1893A3F96EF6E5CD645930E4DC24D118DC0487A578130D3756ABF9438E5C2D2EB1381552EA54EE764B1733BBC6BB2643B9A2B6C8001B911A817AFA5507F1CA4F9890FF6154FC85AE7CC632C7CC66FA05C21FFAF3B')
  datas = get_all_data_for_week(page)

  # Get table of each array and get ONLY 5 days of the week and 10 first elements for others arrays
  all_day_of_weeks = datas[0][5:10]
  all_hour = datas[3][0:10]
  all_course = datas[1][0:10]
  all_course_code = datas[2][0:10]
  all_salle = datas[4][0:10]
  format_datas = []
  for i in range(10):
    hours = format_hours(all_hour[i].text)
    actual_day = all_day_of_weeks[i//2].text
    format_datas.append({
      'day_start': format_date(f'{actual_day} {hours[0]}'), 
      'day_end': format_date(f'{actual_day} {hours[1]}'), 
      'course': format_course(all_course[i].renderContents().decode('utf-8')), 
      'course_code': all_course_code[i].text, 
      'salle': format_salle(all_salle[i].text)
      })

  return format_datas