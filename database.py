import sqlite3

DBNAME = 'youtube.db'

def create_dbs():
    # set connection
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    # Drop tables
    statement = '''
        DROP TABLE IF EXISTS 'Videos';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Authors';
    '''
    cur.execute(statement)
    conn.commit()
    # create a database
    stat = '''
        CREATE TABLE  Authors (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Subscribers INTEGER,
            Channel TEXT
        );
    '''
    cur.execute(stat)
    stat = '''
        CREATE TABLE Videos (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Query TEXT,
            Url TEXT,
            Title TEXT,
            Viewer INTEGER,
            Author TEXT,
            UploadDate TEXT,
            AuthorId INTEGER,
            FOREIGN KEY(AuthorId) REFERENCES Authors(Id)
        );
    '''
    cur.execute(stat)
    conn.commit()
    conn.close()

def get_author_id(author_name):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT Id FROM Authors
        WHERE Name = "{}"
    '''.format(author_name)
    try:
        print(statement)
        cur.execute(statement)
        cid = cur.fetchone()
        conn.close()
        return cid[0]
    except:
        conn.close()
        return None

def insert_video_records(query, video_list):
    # set connection
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    for each in video_list:
        # print("in the loop",each.vnums)
        statement = '''
            INSERT INTO Videos (Query,Url,Title,Viewer,Author,UploadDate,AuthorId)
            VALUES(?,?,?,?,?,?,?)
        '''
        values = (query,each.url,each.title,each.vnums,each.author.name,str(each.date).split(' ')[0],get_author_id(each.author.name))
        # print(statement)
        cur.execute(statement,values)
    conn.commit()
    conn.close()

def insert_author_records(video_list):
    # set connection
    author_list = [v.author for v in video_list]
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    for author in author_list:
        statement = '''
            INSERT INTO Authors (Name,Subscribers,Channel)
            VALUES(?,?,?)
        '''
        values = (author.name,author.subnum,author.channel)
        cur.execute(statement,values)
    conn.commit()
    conn.close()

# test function for time filter function
def filter_time(start,end):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT * FROM Videos
        WHERE date(UploadDate) <= date(?) 
        AND  date(UploadDate) >= date(?)
        ORDER BY date(UploadDate) DESC
    '''
    values = (start,end)
    results = cur.execute(statement,values).fetchall()
    return results

# get stats for daily trend of videos
# params:  start_date, end_date
# return [(date,#videos)]
def get_number_by_date(query,start,end):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT  date(UploadDate) as uploadDate, COUNT(*) AS num  FROM Videos
        WHERE date(UploadDate) <= date(?) 
        AND  date(UploadDate) >= date(?)
        AND Query == ?
        GROUP BY date(UploadDate)
        ORDER BY date(UploadDate) DESC
    '''
    values = (start,end,query)
    results = cur.execute(statement,values).fetchall()
    return results

def get_ranked_videos(query,start,end,top=10):
    print(query,start,end,'----')
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT Title, Author, Viewer, Url FROM Videos
        WHERE date(UploadDate) <= date(?) 
        AND date(UploadDate) >= date(?)
        AND Query == ?
        ORDER BY Viewer DESC
        LIMIT ?
    '''
    values = (start,end,query,top)
    results = cur.execute(statement,values).fetchall()
    print(results)
    return results

def get_popular_authors(query,top=10):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT a.Name AS Author, a.Channel AS Channel, a.Subscribers AS Subscribers, v.Title AS 'Most Recent Video', v.Url AS Link
        FROM Authors AS a JOIN Videos AS v
        ON a.Id = v.AuthorId
        WHERE v.Query = ?
        GROUP BY Author
        HAVING MAX(v.UploadDate)
        ORDER BY Subscribers DESC
        LIMIT ?
    '''
    values = (query,top)
    results = cur.execute(statement,values).fetchall()
    return results

def get_title_list(query):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''
        SELECT Title FROM Videos
        WHERE Query = '{}'
    '''.format(query)
    results = cur.execute(statement).fetchall()
    title_list = [x[0] for x in results]
    return title_list





















