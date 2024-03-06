import sqlite3
import pandas as pd
from chord_classes import Scale, get_chords_for_scale

# OUTLINE FOR C CHORDS - SMALL DATABASE TO VISUALIZE/PRACTICE

# C CHORDS TO CATEGORIZE:
""" 
Triads:
C_MAJ C - E - G
C_MIN C - Eb - G
C_AUG C - E - G#
C_DIM C - Eb - Gb

Diads:
(C_MIN_2): C - C♯
(C_MAJ_2): C - D
(C_MIN_2): C - Db
(C_MIN_3): C - Eb
(C_AUG_2): C - E
(C_DIM_4): C - F
(C_AUG_4): C - F#
(C_PERF_5): C - G
(C_DIM_5): C - Gb
(C_MIN_6): C - Ab
(C_MAJ_6): C - A
(C_AUG_6): C - A#
(C_MIN_7): C - Bb
(C_MAJ_7): C - B

Extended Chords:
(C_MAJ_7): C - E - G - B
(C_DOM_7): C - E - G - Bb
(C_MIN_7): C - Eb - G - Bb
(C_MIN_7_b5): C - Eb - Gb - Bb
(C_DIM_7): C - Eb - Gb - A
(C_7_SUS_4): C - F - G - Bb
(C_MAJ_7_#11): C - E - G - B - F#
(C_DOM_9): C - E - G - Bb - D
(C_MIN_9): C - Eb - G - Bb - D
(C_MAJ_9): C - E - G - B - D
(C_MIN_11): C - Eb - G - Bb - D - F
(C_MAJ_11): C - E - G - B - D - F
(C_MIN_13): C - Eb - G - Bb - D - A
(C_DOM_13): C - E - G - Bb - D - A
(C_MAJ_13): C - E - G - B - D - F - A
Cm(maj7): C Eb G B
Cm(maj9): C Eb G B D
Cm(maj11): C Eb G B D F
Cm(maj13): C Eb G B D F A

"""

conn = sqlite3.connect('chord.db') # in memory databse / easier for testing 

c = conn.cursor()

def get_conn_c():
    conn = sqlite3.connect('chord.db')
    c = conn.cursor()
    return conn, c

# triads, sixths_sevenths, extended = get_chords_for_scale() # returns 3 lists, chord types with lists of chord names with a list of notes

# c.execute(""" CREATE TABLE notes (
#           note_id INTEGER PRIMARY KEY,
#           note_name TEXT
# )""")


# c.execute("""CREATE TABLE triads (
#            chord_name TEXT,
#            tonic TEXT,
#            third TEXT,
#            fifth TEXT
#           )""")

# c.execute("""CREATE TABLE sixths_sevenths (
#           chord_name TEXT,
#           tonic TEXT,
#           second TEXT,
#           third TEXT,
#           fourth TEXT
# )""")

# c.execute("""CREATE TABLE extended (
#           chord_name TEXT,
#           tonic TEXT,
#           second TEXT,
#           third TEXT,
#           fourth TEXT,
#           fifth TEXT,
#           sixth TEXT,
#           seventh TEXT
# )""")


def insert_notes():
    notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    with conn:
        for note in notes:
            c.execute("INSERT INTO notes (note_name) VALUES (?)", (note,))
        

def insert_triads(triads):
    with conn:
        for triad in triads:
            chord_name, tonic, third, fifth = triad # unpack list, 
            c.execute("INSERT INTO triads VALUES (?, ?, ?, ?)", (chord_name, str(tonic), str(third), str(fifth)))

def insert_6ths_7ths(sixths_sevenths):
    with conn:
        for chord in sixths_sevenths:
            chord_name, tonic, second, third, fourth = chord
            c.execute("INSERT INTO sixths_sevenths VALUES (?, ?, ?, ?, ?)", (chord_name, tonic, second, third, fourth))

def insert_extended(extended):
    with conn:
        for chord in extended:
            chord_name, tonic, second, third, fourth, fifth, sixth, seventh = chord
            c.execute("INSERT INTO extended VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (chord_name, tonic, second, third, fourth, fifth, sixth, seventh))

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)   

def display_notes():
    with conn:
        print(pd.read_sql_query("SELECT * FROM notes", conn))

# Function to display db, with pandas (creating a dataframe)
def display_triads():
    with conn:
        print(pd.read_sql_query("SELECT * FROM triads", conn))

def display_6and7s():
    with conn:
        print(pd.read_sql_query("SELECT * FROM sixths_sevenths", conn))

def display_extended():
    with conn:
        print(pd.read_sql_query("SELECT * FROM extended", conn))
        
def find_user_chord(user_notes, conn, c):
    # Create a temporary table for user input
    c.execute("CREATE TEMPORARY TABLE user_input (note_name TEXT)")
    c.executemany("INSERT INTO user_input VALUES (?)", [(note,) for note in user_notes])

    # Get all table names in the database
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'notes';")
    tables = c.fetchall()

    count = 0
    first_matched_chord = None
    other_matched_chords = [] # holds all extra matched notes to send back

    for table in tables:
        table_name = table[0]

        # Get the column names for the chord notes
        c.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in c.fetchall()]

        # Drop the temporary table if it exists
        c.execute("DROP TABLE IF EXISTS chord_counts")

        # Create a temporary table with chord counts
        query = f"""
            CREATE TEMPORARY TABLE chord_counts AS
            SELECT {table_name}.chord_name, COUNT(*) as note_count
            FROM user_input
            JOIN {table_name} ON {' OR '.join(f"user_input.note_name = {table_name}.{column}" for column in columns)}
            GROUP BY {table_name}.chord_name
        """
        c.execute(query)

        # Get all chords with the maximum count of matching notes, from each table
        query_result = c.execute("""
            SELECT chord_name, note_count
            FROM chord_counts 
            WHERE note_count = (SELECT MAX(note_count) FROM chord_counts)
        """).fetchall()

        #print(query_result)

        # Extract the chord and its note_count from each result, and see which ones have the same note count as the users input
        # If several match, return the first found, ignore similar roots, and show options from other chords
        used_tonics = [] # don't repeat tonics, example: c_maj_11 matches with c_maj_13, not good
        for chord, note_count in query_result:
            if note_count == len(user_notes):
                print('here4')
                print(chord)
                print(chord[0] not in used_tonics)
                print(count == 0)
                print(count)
                if chord[0] not in used_tonics and count == 0:
                    first_matched_chord = chord
                    used_tonics.append(chord[0])
                    print(first_matched_chord)
                    print('here')
                    count += 1
                elif chord[0] not in used_tonics:
                    other_matched_chords.append(chord)
                    used_tonics.append(chord[0])
                    count += 1
                     
    if count == 0:
        first_matched_chord = 'No chords were matched!'
        other_matched_chords = 'couldn\'t find any chords'
    elif count == 1:
        other_matched_chords.append(['That was the only chord that matched!'])
    
    return first_matched_chord, other_matched_chords


# insert_triads(triads)s
# insert_notes()
# insert_6ths_7ths(sixths_sevenths)
# insert_extended(extended)
# display_notes()
#display_extended()
# display_6and7s()
# display_triads()
#find_user_chord(user_notes, conn, c)

#conn.close()