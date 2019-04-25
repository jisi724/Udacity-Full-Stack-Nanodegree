#!/usr/bin/env python2.7

import psycopg2


def fetch_data_from_db(query):
    # To fetch data from database with the query statement.
    try:
      db = psycopg2.connect("dbname=news")
    except:
      print ("Unable to connect to the database")
    cursor = db.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    db.close()
    return rows

# What are the most popular three articles of all time?
query1_top3_articles = '''
  select count(*) as num_of_views, a.title as title
  from log as l, articles as a
  where l.status = '200 OK' and LENGTH(l.path) > 1
   and substr(l.path, 10) = a.slug
  group by a.title
  order by num_of_views desc
  limit 3;
'''

# Who are the most popular article authors of all time?
query2_top_author = '''
  select count(*) as num_of_views, au.name
  from log as l, articles as ar, authors as au
  where l.status = '200 OK' and LENGTH(l.path) > 1 and
   substr(l.path, 10) = ar.slug and ar.author  = au.id
  group by ar.author, au.name
  order by num_of_views desc;
'''

# On which days did more than 1% of requests lead to errors?
# Please create views in readme.txt before running this one.
query3_error_date = '''
  select 100 * e.num_of_requests::decimal /
   t.num_of_requests::decimal as percentage, e.date
  from view_error as e, view_total as t
  where e.date = t.date
  order by percentage desc
  limit 1;
'''


def question1_top3_articles():
    data = fetch_data_from_db(query1_top3_articles)
    print ('Queustion1: What are the most popular three articles of all time?')
    for item in data:
        result = '"' + item[1] + '" --- ' + str(item[0]) + ' views'
        print result
    print '\n'


def question2_top_author():
    data = fetch_data_from_db(query2_top_author)
    print ('Queustion2: Who are the most popular article authors of all time?')
    for item in data:
        result = item[1] + ' --- ' + str(item[0]) + ' views'
        print result
    print '\n'


def question3_error_date():
    data = fetch_data_from_db(query3_error_date)[0]
    print ('Queustion3: On which days did more than 1% of requests errors?')
    date = data[1].strftime("%B %d, %Y")
    percentage = '%.2g' % data[0]
    result = str(date) + ' --- ' + str(percentage) + '% views'
    print result


question1_top3_articles()
question2_top_author()
question3_error_date()
