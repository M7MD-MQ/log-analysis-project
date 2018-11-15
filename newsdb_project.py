import bleach
import psycopg2
import datetime

def most_popular_articles():
  """Return the most popular three articles of all time from 'news' , most viewed first."""
  db = psycopg2.connect(database="news")
  c = db.cursor()

  c.execute("SELECT path, count(*) AS num FROM log "
  +"WHERE path = path AND status = '200 OK' AND path !='/'"
  +"GROUP BY path ORDER BY num DESC LIMIT 3")
  q_result = c.fetchall()

  posts = ""
  for post,view in q_result:
      posts += ("\""+post[9:].replace('-',' ').title()+"\""+" — "
      +str(view)+" views"+"\n")
  db.close()
  return posts

def most_popular_authors():
  """Return the most popular article authors of all time from the 'news', most viewed first."""
  db = psycopg2.connect(database="news")
  c = db.cursor()

  c.execute("SELECT name, count(*) AS num "
  +"FROM articles AS a, authors AS au, log AS l "
  +"WHERE a.author = au.id "
  +"AND l.path = CONCAT('/article/',a.slug) "
  +"AND status = '200 OK' AND path !='/' "
  +"GROUP BY au.name ORDER BY num DESC")

  q_result = c.fetchall()

  result = ""
  for auth,view in q_result:
      result += ("\""+auth.replace('-',' ').title()+"\""+" — "
      +str(view)+" views"+"\n")

  db.close()
  return result

def errors_percentage():
  """Return the most popular article authors of all time from the 'news', most viewed first."""
  db = psycopg2.connect(database="news")
  c = db.cursor()

  """ CREATE VIEW date_by_days AS SELECT CAST(time AS DATE) FROM log "
  +"WHERE status != '200 OK' ;"""

  c.execute("SELECT time,(COUNT(time)* 100.00 / (SELECT COUNT(*) FROM date_by_days)) as num "
   +"FROM date_by_days "
   +"GROUP BY time "
   +"HAVING  (COUNT(time)* 100.00 / (SELECT COUNT(*) FROM date_by_days)) > 1 "
   +"ORDER BY num DESC")

  q_result = c.fetchall()
  result=""
  for tim,err in q_result:
      time_re = str(tim)
      dt = datetime.datetime(int(time_re[:4]), int(time_re[5:7]), int(time_re[8:10]))
      result += dt.strftime('%b %d, %Y')+" - "+str(err)[0:3]+"% errors\n"
  db.close()
  return result

if __name__ == '__main__':
      print("The most popular three articles of all time:\n"
      +most_popular_articles())

      print("The most popular article authors of all time:\n"
      +most_popular_authors())

      print("The days where more than 1% of requests lead to errors:\n"
      +str(errors_percentage()))
