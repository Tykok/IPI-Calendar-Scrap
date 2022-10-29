from array import array
from datetime import date
from bs4 import BeautifulSoup
import urllib.request

import dateparser
from ics import Calendar, Event


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

def format_day(day) -> date:
  return dateparser.parse(day).date()

def main() -> array:
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
  page = get_page('ASP.NET_SessionId=swichxnkim2iroomp3uhbfez; .DotNetCasClientAuth=7B4FEF5615896924804735FFB626498ED1F54BED5C5C3E58D1D6792BD85FB7CA74B33F219C309B4AA2C4826C002403373187204D33135BA3904C2AE0EA33F8393CB9E2B7B44F9D4B80EE52FBCEAB21614630D3CA07453F0737F00787454B7D0B648085BE9C132ACD89050E756F8E245E13DFDA8DFFF7CCC34B8EF2AA0F53243286DD54C74E3A85C289C4E5B3E9A06F551C9749AF36A46C998990B9B88B1681736531244D28D58DA7D6815CD44137BD7FEA07D7F826C293A94A0BE19F9CD6C78D7353BD0723AA0B12C18112060E844E4B')
  datas = get_all_data_for_week(page)

  # Get table of each array and get ONLY 5 days of the week
  all_day_of_weeks = datas[0][5:10]
  all_hour = datas[3][0:5]
  all_course = datas[1][0:5]
  all_course_code = datas[2][0:5]
  all_salle = datas[4][0:5]
  format_datas = []
  for i in range(5):
    format_datas.append({
      'day': format_day(all_day_of_weeks[i].text), 
      'hour': format_hours(all_hour[i].text), 
      'course': format_course(all_course[i].renderContents().decode('utf-8')), 
      'course_code': all_course_code[i].text, 
      'salle': format_salle(all_salle[i].text)
      })

  return format_datas