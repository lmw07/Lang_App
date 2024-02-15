'''
This file contains methods to access and modify the database where the sentences are stored.
The database should have 2 tables: sentences and words
'''
import sqlite3
import string
'''
adds sentences from a file. It expects each line of a file to conform to the following format:
norwegian sentence [] english sentence [] norwegian word 1 [] english word 1 [] norwegian word 2 [] english word 2 [] ...
'[]' was arbitrarily chosen as a separator because it is unlikely to appear in the body of a sentence
If sentences are already in database, does not add them or their words
Strips whitespace from beginning and end of words and removes ending punctuation
'''
def add_sentences_from_file(filename : str):
    sentencesList = []
    with open(filename) as file:
        senStringsArr = file.readlines()
    for sentence in senStringsArr:
        sentence = sentence.encode("latin-1").decode("utf-8")
        print(sentence)
        sentence = sentence.replace('"', '')
        sentence = sentence.replace('\n', '')
        sentencesList.append(sentence.split("[]")) 
    
    conn = sqlite3.connect('sentences.db')
    cursor = conn.cursor()
    
    for i in range(0, len(sentencesList)):
        #add the norwegian and english sentence into the sentences table
        norskSentence = sentencesList[i][0]
        engSentence = sentencesList[i][1]
        sentenceQuery = '''INSERT INTO sentences (norsk, english, old, soundfile) SELECT ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM sentences WHERE norsk = ?);'''
        cursor.execute(sentenceQuery,(norskSentence, engSentence, 0, "None", norskSentence))
        conn.commit()
        #if sentences added to sentences table
        if cursor.rowcount == 1:

                # SQL query to get the most recently added primary key
                query = "SELECT sentence_id FROM sentences ORDER BY sentence_id DESC LIMIT 1"

                # Execute the query
                cursor.execute(query)
                
                # Fetch the result
                sentence_id = cursor.fetchone()[0]
                #add to words dictionary
                for j in range(2, len(sentencesList[i]) -1, 2):
                    query = '''INSERT INTO words (sentence_id, norsk, english) VALUES (?,?,?)'''
                    sentencesList[i][j] = cleanString(sentencesList[i][j])
                    sentencesList[i][j+1] = cleanString(sentencesList[i][j+1])
                    cursor.execute(query, (sentence_id, sentencesList[i][j], sentencesList[i][j+1]))
                    conn.commit()
    cursor.close()
    conn.close()
            


    #print(sentencesList)  
    #print(sentencesList[0][0])
    #print(sentencesList[len(sentencesList) -1 ][len(sentencesList[len(sentencesList) -1] ) -1])

'''
Returns input with beginning and ending whitespace and punctuation removed
'''
def cleanString(inString : str) -> str:
    inString = inString.strip()
    translation_table = str.maketrans('', '', string.punctuation)
    cleaned_string = inString.translate(translation_table)
    return cleaned_string







'''
Creates the sentences and words tables
'''
def createTables():
    conn = sqlite3.connect('sentences.db')
    cursor = conn.cursor()

    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS sentences
                    (sentence_id INTEGER PRIMARY KEY, norsk TEXT, english TEXT, old INTEGER, soundfile TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS words (word_id INTEGER PRIMARY KEY, sentence_id INTEGER, norsk TEXT, english TEXT, FOREIGN KEY (sentence_id) REFERENCES sentences (sentence_id))''')
    
    #might add this later if I want to save state between sessions
    #cursor.execute('''CREATE TABLE IF NOT EXISTS workingset (id INTEGER PRIMARY KEY, set_json TEXT);''')

    # Save (commit) the changes
    conn.commit()

    # Query the database
    #cursor.execute('''SELECT * FROM words''')
    #print(cursor.fetchall())

    # Close the cursor and connection
    cursor.close()
    conn.close() 


'''
Gets a random list of sentences, including their english translation and their associated words
PARAM: numberToGet: the number of sentences to fetch. 1/4 of these will be chosen from old sentences
RETURNS:
String list of tuples in format :  norwegian sentence, english sentence, dict{norsk word 1 : english word 1, norsk word 2 : english word 2..., sentence_id
'''
def getSentences(numberToGet : int) -> list:
    # Connect to the SQLite database
    conn = sqlite3.connect('sentences.db')
    cursor = conn.cursor()

    

   
    rows_count = getSizeOfSentenceTable()
    if numberToGet >= 1 and numberToGet <= rows_count:
        # SQL query to fetch 3 random rows
        query = "SELECT * FROM sentences WHERE old = 0 ORDER BY RANDOM() LIMIT ?"

        # Execute the query
        cursor.execute(query, (int(numberToGet * 0.75),))
        random_rows = cursor.fetchall()

        query = "SELECT * FROM sentences WHERE old = 1 ORDER BY RANDOM() LIMIT ?"
        cursor.execute(query, (numberToGet  // 4,))
        random_rows = random_rows + cursor.fetchall()
        # list of rows, each has format [sentence_id, norwegian, english]
        
        sentencesAndWordsList = []
        for row in random_rows:
            #sentencesAndWordsGroup = []
            sentence_id = row[0]
            query = '''SELECT * FROM words WHERE sentence_id = ?'''
            cursor.execute(query, (sentence_id,))
            #sentencesAndWordsGroup.append(row[1])
            #sentencesAndWordsGroup.append(row[2])
            wordsList = cursor.fetchall()
            wordDic = {}

            for wordRow in wordsList:
                wordDic.update({wordRow[2] : wordRow[3]})
                #sentencesAndWordsGroup.append(wordRow[2])
                #sentencesAndWordsGroup.append(wordRow[3])
            
            
            sentencesAndWordsList.append(tuple((row[1], row[2], wordDic, row[0])))
        cursor.close()
        conn.close()
        return sentencesAndWordsList
        #print(sentencesAndWordsList)


def getSizeOfSentenceTable() -> int:
    # Connect to the SQLite database
    conn = sqlite3.connect('sentences.db')
    cursor = conn.cursor()

    # Execute the query to count the rows
    cursor.execute("SELECT COUNT(*) FROM sentences")

    # Fetch the result
    rows_count = cursor.fetchone()[0]
    return rows_count

'''
updates the "old" value of a sentence to reflect that it has been learned or not
'''
def updateSentenceClass(sentence_id : int, learned : bool):
    oldOrNew = 0
    if learned:
        oldOrNew = 1

    # Connect to the SQLite database
    conn = sqlite3.connect('sentences.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE sentences SET old = ? WHERE sentence_id = ?', (oldOrNew,sentence_id))
    conn.commit()
    cursor.close()
    conn.close()



'''
Returns a tuple where the first element is the norwegian sentence and the second element is a filepath to a sound file
'''
def getSentenceSound(sentence_id : int) -> str:
    conn = sqlite3.connect('sentences.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sentences WHERE sentence_id = ?', (sentence_id,))
    out = cursor.fetchall()
    outTup = ((out[0][1], out[0][4]))
    cursor.close()
    conn.close()
    return outTup
    
def updateSentenceSound(sentence_id : int, soundfile: str):
    conn = sqlite3.connect('sentences.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE sentences SET soundfile = ? WHERE sentence_id = ?', (soundfile,sentence_id))
    conn.commit()
    cursor.close()
    conn.close()

'''
removes both tables completely
'''
def __clearTables():
    conn = sqlite3.connect('sentences.db')
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE sentences''')
    cursor.execute('''DROP TABLE words''')
    conn.commit()
    cursor.close()
    conn.close()


def getAllSentenceIds():

    conn = sqlite3.connect("sentences.db")
    cursor = conn.cursor()
    query = "SELECT sentence_id FROM sentences"
    
    try:
        cursor.execute(query)

        sentence_ids = cursor.fetchall()

        sentence_ids = [id[0] for id in sentence_ids]
        
        return sentence_ids
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        cursor.close()
        conn.close()



'''
prints contents of tables for testing
'''
def __test():
    conn = sqlite3.connect('sentences.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM sentences''')
    print(cursor.fetchall())



#print(getSentenceSound(1))
#createTables()
#add_sentences_from_file("sentences_to_add.txt")
#__test()
#__clearTables()
#print(getSentences(3))
#print(getSizeOfSentenceTable())










