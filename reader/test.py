from datetime import datetime
import time
from time import mktime
from operator import itemgetter

import feedparser
import sqlite3

# article = (u'test article', u'http://www.mattdinauta.com', u'test article', 4, 1, u'2013-07-19 23:20:31')
# connect = sqlite3.connect("../informed/informed.db")
# cursor = connect.cursor()
# for feed_tutle, url, article_title, user, feed, date in article:
# 	print url
# 	# if url == []:
# 	# 	print True
# 	# else:
# 	# 	print False
# # select = "SELECT * FROM reader_Article WHERE url = 'http://www.mattdinauta.com'"
# # cursor.execute(select)
# # data = cursor.fetchall()



# # for r in data:
# #     print r


# # (u'test article', u'http://www.mattdinauta.com', u'test article', 4, 1, u'2013-07-19 23:20:31')

print datetime.today()

today_str = str(datetime.today())
print today_str
print type(today_str)