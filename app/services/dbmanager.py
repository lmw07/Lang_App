

'''
This file contains methods to access and modify the database where the sentences are stored.
The database should have 2 tables: sentences and words
'''
import sqlite3
import string
from app.models.sentence import Sentence
import app.constants as constants

dbPath = constants.DB_PATH






'''
adds sentences from a file. Each line of the file should be a JSON of a sentence object.
Here is an example
{"Norwegian_sentence": "Jeg liker å lese bøker om vinteren", "English_translation": "I like to read books in the winter",
 "Word_mapping": {"Jeg": "I", "liker": "like", "å": "to", "lese": "read", "bøker": "books", "om": "in", "vinteren": "the winter"}}

'''
def add_sentences_from_file(filename : str):

    with open(filename) as file:
        senStringsArr = file.readlines()
        senStringsArr = [sentence.encode("latin1").decode("utf-8") for sentence in senStringsArr]
        senStringsArr = [sentence.replace("Ã¥", "å").replace("Ã¦","æ" ).replace("Ã¸", "ø") for sentence in senStringsArr]

    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    
    for sentence in senStringsArr:

        sentenceObject = Sentence(sentence)

        #add the norwegian and english sentence into the sentences table
        norskSentence = sentenceObject.norwegian
        engSentence = sentenceObject.english
        sentenceQuery = '''INSERT INTO sentences (norsk, english, old, soundfile) SELECT ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM sentences WHERE norsk = ?);'''
        cursor.execute(sentenceQuery,(norskSentence, engSentence, 0, "None", norskSentence))
        conn.commit()
        #if sentences added to sentences table, add words to words table
        if cursor.rowcount == 1:

                # SQL query to get the most recently added primary key
                query = "SELECT sentence_id FROM sentences ORDER BY sentence_id DESC LIMIT 1"

                # Execute the query
                cursor.execute(query)
                
                # Fetch the result
                sentence_id = cursor.fetchone()[0]
                #add to words dictionary
                for key in sentenceObject.word_map:
                    query = '''INSERT INTO words (sentence_id, norsk, english) VALUES (?,?,?)'''
                    cleanedNorskWord = cleanString(key)
                    cleanedEngWord = cleanString(sentenceObject.word_map[key])
                    cursor.execute(query, (sentence_id, cleanedNorskWord,cleanedEngWord))
                    conn.commit()

    cursor.close()
    conn.close()
            

'''
Returns input with beginning and ending whitespace and punctuation removed
'''
def cleanString(inString : str) -> str:
    inString = inString.strip()
    translation_table = str.maketrans('', '', string.punctuation)
    cleaned_string = inString.translate(translation_table)
    return cleaned_string

'''
Adds a sentence from a sentence object
'''
def addSentence(sentence : Sentence):
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    sentenceQuery = '''INSERT INTO sentences (norsk, english, old, soundfile) 
    SELECT ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM sentences WHERE norsk = ?);'''
    cursor.execute(sentenceQuery,(sentence.norwegian, sentence.english, 0, "None", sentence.norwegian))
    conn.commit()
    if cursor.rowcount == 1:

        # SQL query to get the most recently added primary key
        query = "SELECT sentence_id FROM sentences ORDER BY sentence_id DESC LIMIT 1"

        # Execute the query
        cursor.execute(query)

        # Fetch the result
        sentence_id = cursor.fetchone()[0]
        #add to words dictionary
        for key in sentence.word_map:
            query = '''INSERT INTO words (sentence_id, norsk, english) VALUES (?,?,?)'''
            cleanedNorskWord = cleanString(key)
            cleanedEngWord = cleanString(sentence.word_map[key])
            cursor.execute(query, (sentence_id, cleanedNorskWord,cleanedEngWord))
            conn.commit()

'''
Gets the number of known sentences
'''
def getCountKnownSentences():
    # Connect to the SQLite database
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()

    # Execute the query to count the rows
    cursor.execute("SELECT COUNT(*) FROM sentences WHERE old = 1")

    # Fetch the result
    rows_count = cursor.fetchone()[0]
    return rows_count


def getSentencesFromWord(word :str) -> list:
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    query = "SELECT * FROM sentences WHERE norsk LIKE ?"
    param = f"%{word}%"
    cursor.execute(query, (param,))
    
    random_rows = cursor.fetchall()
    
    sentencesAndWordsList = []
    for row in random_rows:
 
        sentence_id = row[0]
        query = '''SELECT * FROM words WHERE sentence_id = ?'''
        cursor.execute(query, (sentence_id,))
      
        wordsList = cursor.fetchall()
        wordDic = {}

        for wordRow in wordsList:
            wordDic.update({wordRow[2] : wordRow[3]})
    
        
        
        sentencesAndWordsList.append(tuple((row[1], row[2], wordDic, row[0])))
        out = []
        for tup in sentencesAndWordsList:
            out.append(Sentence(tup[0], tup[1], tup[2], tup[3]))
    cursor.close()
    conn.close()
    return out

'''
Creates the sentences and words tables
'''
def createTables():
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()

    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS sentences
                    (sentence_id INTEGER PRIMARY KEY, norsk TEXT, english TEXT, old INTEGER, soundfile TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS words (word_id INTEGER PRIMARY KEY, sentence_id INTEGER, norsk TEXT, english TEXT, FOREIGN KEY (sentence_id) REFERENCES sentences (sentence_id))''')
    
    #might add this later if I want to save state between sessions
    #cursor.execute('''CREATE TABLE IF NOT EXISTS workingset (id INTEGER PRIMARY KEY, set_json TEXT);''')

  
    conn.commit()



    # Close the cursor and connection
    cursor.close()
    conn.close() 


'''
Gets a random list of sentences, including their english translation and their associated words

PARAM: numberToGet: the number of sentences to fetch.
PARAM: status: must be 'OLD' or 'NEW'. Indicates whether to return learned or new sentences
RETURNS: list of sentences
'''
def getRandomSentences(numberToGet : int, status = 'NEW') -> list:
    if status != "OLD" and status != "NEW":
        raise ValueError("Invalid status. Must be OLD or NEW")
    
    statusNum = 1
    if status == "NEW":
        statusNum = 0
    # Connect to the SQLite database
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    rows_count = getSizeOfSentenceTable()
    if numberToGet >= 1 and numberToGet <= rows_count:
        # SQL query to fetch 3 random rows
        query = "SELECT * FROM sentences WHERE old = ? ORDER BY RANDOM() LIMIT ?"

        # Execute the query
        cursor.execute(query, (statusNum, numberToGet,))
        random_rows = cursor.fetchall()
        
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
            out = []
            for tup in sentencesAndWordsList:
                out.append(Sentence(tup[0], tup[1], tup[2], tup[3]))
        cursor.close()
        conn.close()
        return out
        #print(sentencesAndWordsList)


def getSizeOfSentenceTable() -> int:
    # Connect to the SQLite database
    conn = sqlite3.connect(dbPath)
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
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute('UPDATE sentences SET old = ? WHERE sentence_id = ?', (oldOrNew,sentence_id))
    conn.commit()
    cursor.close()
    conn.close()




'''
Returns a tuple where the first element is the norwegian sentence and the second element is a filepath to a sound file
'''
def getSentenceSound(sentence_id : int) -> str:
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sentences WHERE sentence_id = ?', (sentence_id,))
    out = cursor.fetchall()
    outTup = ((out[0][1], out[0][4]))
    cursor.close()
    conn.close()
    return outTup
    
def updateSentenceSound(sentence_id : int, soundfile: str):
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute('UPDATE sentences SET soundfile = ? WHERE sentence_id = ?', (soundfile,sentence_id))
    conn.commit()
    cursor.close()
    conn.close()



def getAllSentenceIds():

    conn = sqlite3.connect(dbPath)
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
Delete all data associated with a particular norsk sentence using its Norwegian sentence or its sentence id
'''
def deleteSentence(sentence_id : int = None, norskSentence :string = None):
    if not sentence_id and not norskSentence:
        raise Exception("Must provide either sentence id or Norwegian text")
    try:
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()
        if not sentence_id:
            findSentenceIdCommand = "SELECT * FROM sentences WHERE norsk = ?"
            cursor.execute(findSentenceIdCommand, (norskSentence,))
            out = cursor.fetchall()
            sentence_id = out[0][0]
        else:
            sentence_id = str(sentence_id)
        deleteWordsCommand = "DELETE FROM words WHERE sentence_id = ?"
        cursor.execute(deleteWordsCommand, (sentence_id,))
        deleteSentenceCommand = "DELETE FROM sentences WHERE sentence_id = ?"
        cursor.execute(deleteSentenceCommand, (sentence_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()



'''
prints contents of tables for testing
'''
def __print_table__(table):
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table}')
    print(cursor.fetchall())


'''
Run this if some of the special characters in the sentences are corrupt
'''
def __fix_encodingInWholeDB__(db_path, table_name, column_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query to fetch all rows from the specified table and column
    cursor.execute(f"SELECT rowid, {column_name} FROM {table_name}")
    rows = cursor.fetchall()
    
    # Iterate through all fetched rows
    for row_id, text in rows:
        try:
            
            corrected_text = text.replace("Ã¥", "å").replace("Ã¦","æ" ).replace("Ã¸", "ø")
            # Update the row with the corrected text
            cursor.execute(f"UPDATE {table_name} SET {column_name} = ? WHERE rowid = ?", (corrected_text, row_id))
        except UnicodeEncodeError:
            # If there's an encoding error, skip the update for this row
            print(f"Skipping row {row_id} due to encoding issues.")
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("Database update complete.")
    
'''
Run this if the sound file paths are incorrect
'''
def __fixsound__():
     # Connect to the SQLite database
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    
    # Query to fetch all rows from the specified table and column
    cursor.execute(f"SELECT rowid, soundfile FROM sentences")
    rows = cursor.fetchall()
    for row_id, text in rows:
        if len(text) <5:
            #correctedFile = text[12:]
            cursor.execute(f"UPDATE sentences SET soundfile = ? WHERE rowid = ?", (str(row_id) + ".mp3", row_id))
    conn.commit()
    conn.close()
    print('done')

