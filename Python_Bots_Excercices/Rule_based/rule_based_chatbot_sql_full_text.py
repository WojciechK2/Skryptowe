import sqlite3

welcome = "Hi! I'm Arthur, the customer support chatbot. How can I help you?"


#Creating and inserting values into db
conn = sqlite3.connect('fulltext_chatbot.sqlite')
conn.enable_load_extension(True)
conn.load_extension('fts5')

conn.execute("CREATE VIRTUAL TABLE responses USING fts5(question,answer)")
db_cursor = conn.cursor()
db_cursor.execute('INSERT INTO responses(question,answer) VALUES(\"The app if freezing after I click run button\",\"You need to clean up the cache. Please go to ...\");')
db_cursor.execute('INSERT INTO responses(question,answer) VALUES(\"I don t know how to proceed with the invoice\",\"Please go to Setting, next Subscriptions and there is the Billing section\");')
db_cursor.execute('INSERT INTO responses(question,answer) VALUES(\"I get an error when I try to install the app\",\"Could you plese send the log files placed in ... to ...\");')
db_cursor.execute('INSERT INTO responses(question,answer) VALUES(\"It crash after I have updated it\",\"Please restart your PC\");')
db_cursor.execute('INSERT INTO responses(question,answer) VALUES(\"I cannot login in to the app\",\"Use the forgot password button to setup a new password\");')
db_cursor.execute('INSERT INTO responses(question,answer) VALUES(\"I m not able to download it\",\"Probably you have an ad blocker plugin installed and it blocks the popup with the download link\");')
conn.commit()

def db_search(question):
	db_cursor = conn.cursor()
	db_cursor.execute("SELECT answer, bm25(responses) FROM responses WHERE responses MATCH 'question: \"+str(question)+\"' ORDER BY bm25(responses) LIMIT 0,1;")
	return_string = db_cursor.fetchall()
	return return_string

def get_highest_similarity(question):
	return db_search(question)

def run_chatbot():
    print(welcome)
    question = ""
    while question != "thank you":
        question = input()
        answer = get_highest_similarity(question)
        print(answer)
    
run_chatbot()


