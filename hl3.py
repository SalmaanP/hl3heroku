import praw
from time import sleep
import re
import os
import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)


#login
u_name=os.environ['reddit_uname']
p_word=os.environ['reddit_pword']
r = praw.Reddit(user_agent='hl3_confirmer_bot by u/sallurocks version 1.0')
#r.http.proxies = {'http': "http://hl3_confirmer_bot:prawisgood@proxy.iisc.ernet.in:3128"}
r.login(u_name,p_word)




#subreddit = r.get_subreddit('gaming')
#flat_comments = subreddit.get_comments()



condition = True
msg="Thank you for confirming Half-Life 3, your outstanding logical and mathematical skills will forever be remembered.\n\n\nYour confirmation is being confirmed for future reference\n\n______________________________\n\nCurrent confirmation count:"
keyword={'hl3 confirmed','hl3 confirm','hl confirm','hl 3 confirm','hl confirmed','hl 3 confirmed','half life confirm','half life 3 confirm','half-life 3 confirmed','halflife3 confirmed','half life3 confirm','half-life3 confirm','hl3 is confirmed','half life 3 is confirmed','half-life 3 is confirmed','hl 3 is confirmed','half life 3 - confirmed','half life 3 is now officially confirmed','half-life 3 is now official confirmed','half-life 3 confirmed!','hl three confirmed','half life three confirmed','half-life three confirmed'}
notkeyword={'"HL3 confirmed"','"Half-life 3 confirmed"','"Half life 3 confirmed"'}
endmsg="\n\n\n\n\n[^^Message ^^The ^^Confirmaster](http://www.reddit.com/message/compose/?to=sallurocks)       [^^Source](https://github.com/HunkDivine/herokuhl3)"
while condition:


    cur = conn.cursor()
    cur.execute("""SELECT counts from confirmations""")
    rows = cur.fetchall()
    count=0
    for row in rows:
        count=row[0]
	
    #a+ to append everytime
    fo=open("test.txt","a+")
    f1=open("count.txt","r+")
    f2=open("archive.txt","a+")

    #count=f1.read()
    count=int(count)

    #to read the entire file and check id to prevent duplicate posts
    #need to seek pointer to the beginning and put it back at the end
    position=fo.tell()
    fo.seek(0,0)
    str=fo.read()
    fo.seek(position)


    #submissions = r.get_submission(submission_id='38kwdj')
    #flat_comments = praw.helpers.flatten_tree(submissions.comments)
    subreddit = r.get_subreddit('pcmasterrace+halflife+globaloffensive+TESTBOTTEST+casualconversation')
    flat_comments = subreddit.get_comments()
    try:
        for comment in flat_comments:
            for value in keyword:
                
                if( ( value in comment.body.lower() ) and (comment.id not in str) ):

                    print('Ok!')
                    print(comment.body)
                    count=count+1
                    cur.execute("""UPDATE confirmations SET counts = %s;""", (count,))
                    conn.commit()
                    comment.reply(msg+"%s" % count+endmsg)
                    fo.write(comment.id+" ")
                    f1.seek(0,0)
                    f2.write("Count %s\n" % count)
                    f2.write(comment.body)
                    f2.write("\n\n")
                    f1.write("%s" % count)
                    break;
                    
           
                else:
                    print("No")
                    print((comment.body).encode('utf-8','replace'))

    except KeyboardInterrupt:
        running = False
    except praw.errors.APIException:
        print "[ERROR]:"
        print "sleeping 300 sec"
        sleep(300)
    except Exception as e: # In reality you don't want to just catch everything like this, but this is toy code.
	print Exception      
	print e
	print "[ERROR]:"
        print "blindly handling error"
        continue
            
            

    fo.close()
    f1.close()
    f2.close()
    sleep(5)
