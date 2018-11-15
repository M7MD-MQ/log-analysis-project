# Log Analysis Project
This is a simple project which is part of the requirements of passing the _Udacity_ course, the goal of this project is to build an internal reporting tool that will use information from the database to discover what  kind of articles the site's readers like, the database contains newspaper articles, as well as the web server log for the site, the log has a database row for each time a reader loaded a web page.

## Here Are The Questions The Reporting Tool Should Answer
1. What are the most popular three articles of all time?

2. Who are the most popular article authors of all time?

3.  On which days did more than 1% of requests lead to errors?

## Installation

- Vagrant:	https://www.vagrantup.com/downloads.html

- VirtualMachine:	https://www.virtualbox.org/wiki/Downloads

- Download	a	FSND	virtual	machine:	https://github.com/udacity/fullstack-nanodegree-vm

- You	will	also	need	a	Unix-style	terminal	program

- For	this	project,you	need	to	download	“newsdata.sql”from	the	project	page	or	by	clicking	on	the	following	link:	https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

- `pip3 install psycopg2`

- `pip3 install pycodestyle`

## Database Table Description
- **Authors**: table includes information about the authors of articles.

- **Articles**: table includes the articles themselves.

- **Log**: table includes one entry for each time a user has accessed the site.

- **date_by_days**: a view table contain only one column called date formatted as: `YY-MM-DD`.

This view created by this command:
`CREATE VIEW date_by_days AS SELECT CAST(time AS DATE) FROM log "+"WHERE status != '200 OK'`

## Code Explanation
 ### Imported Library:
- `import psycopg2` : this library used for connecting to database.

- `import datetime` : this library used for converting the time format.

### Functions:
1. `def most_popular_articles()` : this function return the most popular three articles of all time from 'news' , most viewed first.

2. `def most_popular_authors()` : this function return the most popular article authors of all time from the 'news', most viewed first.

3. `def errors_percentage()` : this function return the most popular article authors of all time from the 'news', most viewed first.

### Database Connection
This following statements applies the same for all functions:

- `db = psycopg2.connect(database="news")`: we use this statment to connect to the database, in this case our database called _news_ .

- `c = db.cursor()`: we use this statment to create the database pointer which is used to retrieve data.

- `db.close()` : we use this statment to close the communication with the database.

- `c.execute(query)`: we use this statment to excute the _SQL_ query(plase the query inside the parentheses).

- `c.fetchall()`: we use this statment to return the result as an array.

### Queries
1. To get the most popular three articles:
```
c.execute("SELECT path, count(*) AS num FROM log "
  +"WHERE path = path AND status = '200 OK' AND path !='/'"
  +"GROUP BY path ORDER BY num DESC LIMIT 3")
```
2. to get the the most popular article authors:
```
c.execute("SELECT name, count(*) AS num "
  +"FROM articles AS a, authors AS au, log AS l "
  +"WHERE a.author = au.id "
  +"AND l.path = CONCAT('/article/',a.slug) "
  +"AND status = '200 OK' AND path !='/' "
  +"GROUP BY au.name ORDER BY num DESC")
  ```

2. to get the which days did more than 1% of requests lead to errors:
```
c.execute("SELECT time,(COUNT(time)* 100.00 / (SELECT COUNT(*) FROM date_by_days)) as num "
   +"FROM date_by_days "
   +"GROUP BY time "
   +"HAVING  (COUNT(time)* 100.00 / (SELECT COUNT(*) FROM date_by_days)) > 1 "
   +"ORDER BY num DESC")
```

### Data Representation

`for V1,V2 in q_result:` : all the function use the same method, however in order to reorganize the data as expected, i did used loop to go through the array, the first arrgement _V1_ represented as a string, and the second arrgement _V2_ represented as a number.

The difference appeared in the body of the loop, and here the explanation of that:

1. `posts += ("\""+post[9:].replace('-',' ').title()+"\""+" — "+str(view)+" views"+"\n")`: take every thing after the 9th position and replace all the '-' with spaces, then capitalize the first letter in every string to meet the requirement form.


2. `result += ("\""+auth.replace('-',' ').title()+"\""+" — "+str(view)+" views"+"\n")`: replace all the '-' with spaces, then capitalize the first letter in every string to meet the requirement form.

3. `time_re = str(tim)`:convert _time_ to _string_, i did this to divide the time into YY:MM:DD then change the format as what is required.
      `dt = datetime.datetime(int(time_re[:4]), int(time_re[5:7]), int(time_re[8:10]))
      result += dt.strftime('%b %d, %Y')+" - "+str(err)[0:3]+"% errors\n"`: here i use datetime to convert from YY:MM:DD to the required format, where `time_re[:4]` is the year, and `time_re[5:7]` is the month, and `time_re[8:10]` is the day, then by using `strftime('%b %d, %Y')`, where `%b` is the month in letter form like(Jul), and `%d` is the day in number form like(22), and `%Y` is the year in number form like(1999). The `str(err)[0:3]` to take only three number(two before the point and one after).
