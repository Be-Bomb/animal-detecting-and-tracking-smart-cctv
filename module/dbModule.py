import sqlite3
import pandas as pd
import numpy as np


class Database():
    def __init__(self):
        self.conn = sqlite3.connect('capstone_db.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

    def insertInfo(self, object):
        self.cursor.execute(
            "INSERT INTO {} (detected_date, detected_time) VALUES(strftime('%Y-%m-%d', 'now', 'localtime'), strftime('%H:%M:%S', 'now', 'localtime'));".format(object))
        self.conn.commit()

    def selectByTimeObject(self, object):
        query1 = """
        SELECT count(id) FROM {}
        WHERE (detected_date = strftime('%Y-%m-%d', 'now', 'localtime') 
        AND (detected_time BETWEEN '00:00:00' AND '02:59:59'));
        """.format(object)
        df1 = pd.read_sql_query(query1, self.conn)
        _0to3 = int(df1['count(id)'].values)

        query2 = """
        SELECT count(id) FROM {}
        WHERE (detected_date = strftime('%Y-%m-%d', 'now', 'localtime') 
        AND (detected_time BETWEEN '03:00:00' AND '05:59:59'));
        """.format(object)
        df2 = pd.read_sql_query(query2, self.conn)
        _3to6 = int(df2['count(id)'].values)

        query3 = """
        SELECT count(id) FROM {}
        WHERE (detected_date = strftime('%Y-%m-%d', 'now', 'localtime') 
        AND (detected_time BETWEEN '06:00:00' AND '08:59:59'));
        """.format(object)
        df3 = pd.read_sql_query(query3, self.conn)
        _6to9 = int(df3['count(id)'].values)

        query4 = """
        SELECT count(id) FROM {}
        WHERE (detected_date = strftime('%Y-%m-%d', 'now', 'localtime') 
        AND (detected_time BETWEEN '09:00:00' AND '20:59:59'));
        """.format(object)
        df4 = pd.read_sql_query(query4, self.conn)
        _etc = int(df4['count(id)'].values)

        query5 = """
        SELECT count(id) FROM {}
        WHERE (detected_date = strftime('%Y-%m-%d', 'now', 'localtime') 
        AND (detected_time BETWEEN '21:00:00' AND '23:59:59'));
        """.format(object)
        df5 = pd.read_sql_query(query5, self.conn)
        _21to24 = int(df5['count(id)'].values)

        timeCnt = [_21to24, _0to3, _3to6, _6to9, _etc]

        return timeCnt

    def selectByTimeObjectWeekly(self, object):
        query1 = """
        SELECT count(id) FROM {}
        WHERE (detected_date BETWEEN strftime('%Y-%m-%d', 'now', 'localtime''-6 day') 
        AND strftime('%Y-%m-%d', 'now', 'localtime')) AND (detected_time BETWEEN '00:00:00' AND '02:59:59');
        """.format(object)
        df1 = pd.read_sql_query(query1, self.conn)
        _0to3 = int(df1['count(id)'].values)

        query2 = """
        SELECT count(id) FROM {}
        WHERE (detected_date BETWEEN strftime('%Y-%m-%d', 'now', 'localtime', '-6 day') 
        AND strftime('%Y-%m-%d', 'now', 'localtime')) AND (detected_time BETWEEN '03:00:00' AND '05:59:59');
        """.format(object)
        df2 = pd.read_sql_query(query2, self.conn)
        _3to6 = int(df2['count(id)'].values)

        query3 = """
        SELECT count(id) FROM {}
        WHERE (detected_date BETWEEN strftime('%Y-%m-%d', 'now', 'localtime', '-6 day') 
        AND strftime('%Y-%m-%d', 'now', 'localtime')) AND (detected_time BETWEEN '06:00:00' AND '08:59:59');
        """.format(object)
        df3 = pd.read_sql_query(query3, self.conn)
        _6to9 = int(df3['count(id)'].values)

        query4 = """
        SELECT count(id) FROM {}
        WHERE (detected_date BETWEEN strftime('%Y-%m-%d', 'now', 'localtime', '-6 day') 
        AND strftime('%Y-%m-%d', 'now', 'localtime')) AND (detected_time BETWEEN '09:00:00' AND '20:59:59');
        """.format(object)
        df4 = pd.read_sql_query(query4, self.conn)
        _etc = int(df4['count(id)'].values)

        query5 = """
        SELECT count(id) FROM {}
        WHERE (detected_date BETWEEN strftime('%Y-%m-%d', 'now', 'localtime', '-6 day') 
        AND strftime('%Y-%m-%d', 'now', 'localtime')) AND (detected_time BETWEEN '21:00:00' AND '23:59:59');
        """.format(object)
        df5 = pd.read_sql_query(query5, self.conn)
        _21to24 = int(df5['count(id)'].values)

        timeCnt = [_21to24, _0to3, _3to6, _6to9, _etc]

        return timeCnt

    def selectByTimeObjectTotal(self, object):
        query1 = """
        SELECT count(id) FROM {}
        WHERE (detected_time BETWEEN '00:00:00' AND '02:59:59');
        """.format(object)
        df1 = pd.read_sql_query(query1, self.conn)
        _0to3 = int(df1['count(id)'].values)

        query2 = """
        SELECT count(id) FROM {}
        WHERE (detected_time BETWEEN '03:00:00' AND '05:59:59');
        """.format(object)
        df2 = pd.read_sql_query(query2, self.conn)
        _3to6 = int(df2['count(id)'].values)

        query3 = """
        SELECT count(id) FROM {}
        WHERE (detected_time BETWEEN '06:00:00' AND '08:59:59');
        """.format(object)
        df3 = pd.read_sql_query(query3, self.conn)
        _6to9 = int(df3['count(id)'].values)

        query4 = """
        SELECT count(id) FROM {}
        WHERE (detected_time BETWEEN '09:00:00' AND '20:59:59');
        """.format(object)
        df4 = pd.read_sql_query(query4, self.conn)
        _etc = int(df4['count(id)'].values)

        query5 = """
        SELECT count(id) FROM {}
        WHERE (detected_time BETWEEN '21:00:00' AND '23:59:59');
        """.format(object)
        df5 = pd.read_sql_query(query5, self.conn)
        _21to24 = int(df5['count(id)'].values)

        timeCnt = [_21to24, _0to3, _3to6, _6to9, _etc]

        return timeCnt

    def selectByTime(self):
        deer_cnt = self.selectByTimeObject("water_deer")
        pig_cnt = self.selectByTimeObject("wild_pig")
        cat_cnt = self.selectByTimeObject("cat")
        person_cnt = self.selectByTimeObject("person")

        return [deer_cnt, pig_cnt, cat_cnt, person_cnt]

    def selectByTimeWeekly(self):
        deer_cnt = self.selectByTimeObjectWeekly("water_deer")
        pig_cnt = self.selectByTimeObjectWeekly("wild_pig")
        cat_cnt = self.selectByTimeObjectWeekly("cat")
        person_cnt = self.selectByTimeObjectWeekly("person")

        return [deer_cnt, pig_cnt, cat_cnt, person_cnt]

    def selectByTimeTotal(self):
        deer_cnt = self.selectByTimeObjectTotal("water_deer")
        pig_cnt = self.selectByTimeObjectTotal("wild_pig")
        cat_cnt = self.selectByTimeObjectTotal("cat")
        person_cnt = self.selectByTimeObjectTotal("person")

        return [deer_cnt, pig_cnt, cat_cnt, person_cnt]

    def selectTodayAll(self):
        query1 = """
        SELECT count(id) FROM water_deer
        WHERE (detected_date = strftime('%Y-%m-%d', 'now', 'localtime'));
        """
        df1 = pd.read_sql_query(query1, self.conn)
        deer_cnt = int(df1['count(id)'].values)

        query2 = """
        SELECT count(id) FROM wild_pig
        WHERE (detected_date = strftime('%Y-%m-%d', 'now', 'localtime'));
        """
        df2 = pd.read_sql_query(query2, self.conn)
        pig_cnt = int(df2['count(id)'].values)

        query3 = """
        SELECT count(id) FROM cat
        WHERE (detected_date = strftime('%Y-%m-%d', 'now', 'localtime'));
        """
        df3 = pd.read_sql_query(query3, self.conn)
        cat_cnt = int(df3['count(id)'].values)

        query4 = """
        SELECT count(id) FROM person
        WHERE (detected_date = strftime('%Y-%m-%d', 'now', 'localtime'));
        """
        df4 = pd.read_sql_query(query4, self.conn)
        person_cnt = int(df4['count(id)'].values)

        today_cnt = [deer_cnt, pig_cnt, cat_cnt, person_cnt]
        return today_cnt

    def selectWeeklyAll(self):
        query1 = """
        SELECT count(id) FROM water_deer
        WHERE (detected_date BETWEEN strftime('%Y-%m-%d', 'now', 'localtime', '-6 day') AND strftime('%Y-%m-%d', 'now', 'localtime'));
        """
        df1 = pd.read_sql_query(query1, self.conn)
        deer_cnt = int(df1['count(id)'].values)

        query2 = """
        SELECT count(id) FROM wild_pig
        WHERE (detected_date BETWEEN strftime('%Y-%m-%d', 'now', 'localtime', '-6 day') AND strftime('%Y-%m-%d', 'now', 'localtime'));
        """
        df2 = pd.read_sql_query(query2, self.conn)
        pig_cnt = int(df2['count(id)'].values)

        query3 = """
        SELECT count(id) FROM cat
        WHERE (detected_date BETWEEN strftime('%Y-%m-%d', 'now', 'localtime', '-6 day') AND strftime('%Y-%m-%d', 'now', 'localtime'));
        """
        df3 = pd.read_sql_query(query3, self.conn)
        cat_cnt = int(df3['count(id)'].values)

        query4 = """
        SELECT count(id) FROM person
        WHERE (detected_date BETWEEN strftime('%Y-%m-%d', 'now', 'localtime', '-6 day') AND strftime('%Y-%m-%d', 'now', 'localtime'));
        """
        df4 = pd.read_sql_query(query4, self.conn)
        person_cnt = int(df4['count(id)'].values)

        weekly_cnt = [deer_cnt, pig_cnt, cat_cnt, person_cnt]
        return weekly_cnt

    def selectAll(self):
        query1 = "SELECT count(id) FROM water_deer"
        df1 = pd.read_sql_query(query1, self.conn)
        deer_cnt = int(df1['count(id)'].values)

        query2 = "SELECT count(id) FROM wild_pig"
        df2 = pd.read_sql_query(query2, self.conn)
        pig_cnt = int(df2['count(id)'].values)

        query3 = "SELECT count(id) FROM cat"
        df3 = pd.read_sql_query(query3, self.conn)
        cat_cnt = int(df3['count(id)'].values)

        query4 = "SELECT count(id) FROM person"
        df4 = pd.read_sql_query(query4, self.conn)
        person_cnt = int(df4['count(id)'].values)

        all_cnt = [deer_cnt, pig_cnt, cat_cnt, person_cnt]
        return all_cnt

    # def selectLongTermObject(self, object, term):
    #     # term: 7/30
    #     query = """
    #     SELECT detected_date, count(id) FROM {}
    #     WHERE (detected_date BETWEEN strftime('%Y-%m-%d', 'now', 'localtime', '-{} day') AND strftime('%Y-%m-%d', 'now', 'localtime'))
    #     GROUP BY detected_date;
    #     """.format(object, term)
    #     df = pd.read_sql_query(query, self.conn)
    #     date = df['detected_date'].tolist()
    #     cnt = df['count(id)'].tolist()
    #     pairs = dict(zip(date, cnt))

    #     return pairs

    # def selectLongTerm(self, term):
    #     deer_cnt = self.selectLongTermObject("water_deer", term)
    #     pig_cnt = self.selectLongTermObject("wild_pig", term)
    #     cat_cnt = self.selectLongTermObject("cat", term)
    #     person_cnt = self.selectLongTermObject("person", term)
    #     return [deer_cnt, pig_cnt, cat_cnt, person_cnt]

    def insertPushMessage(self, noti_date, msg):
        self.cursor.execute(
            "INSERT INTO notification (noti_datetime, msg) VALUES('{}', '{}');".format(noti_date, msg))
        self.conn.commit()

    def sendNotiList(self):
        query = "SELECT * FROM notification WHERE (strftime('%Y-%m-%d', noti_datetime) = strftime('%Y-%m-%d', 'now', 'localtime'));"
        df = pd.read_sql_query(query, self.conn)
        notiList = []
        for i in range(len(df)):
            tmp = [str(df['id'][i]), df['noti_datetime'][i], df['msg'][i]]
            notiList.append(tmp)
        notiList = list(reversed(notiList))
        return notiList

    def removeNoti(self, idx):
        self.cursor.execute(
            "DELETE FROM notification WHERE id = {};".format(idx)
        )
        self.conn.commit()

# Test
# db = Database()
# db.sendNotiList()
