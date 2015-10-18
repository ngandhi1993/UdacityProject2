#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from ast import literal_eval as make_tuple
def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    c.execute("DELETE FROM Matches")

def deletePlayers():
    """Remove all the player records from the database."""
    c.execute("DELETE FROM Players")

def countPlayers():
    """Returns the number of players currently registered."""
    c.execute("SELECT COUNT(*) FROM Players")
    numRecords = c.fetchone()
    return numRecords[0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    query = 'INSERT INTO Players (PlayerName) VALUES (%s);'
    params = (name, )
    c.execute(query, params)

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    tuples = []
    c.execute('Select (PlayerID, PlayerName, GamesWon, GamesPlayed) From Players ORDER BY GamesWon DESC')
    fetchall = c.fetchall()
    results = [element for (element,) in fetchall]
    for result in results:
        row = result[1:-1].split(',')
        tuple = (int(row[0]), returnName(str(row[1])), int(row[2]), int(row[3]))
        tuples.append(tuple)
    return tuples

def returnName(name):
    """Rectifies discrepancies in the name returned by P-SQL

    Args:
        name: the player's full name with or without double quotes

    Returns:
        Player's full name excluding the quotes
    """
    if name[0] == '\"':
        return name[1:-1]
    else:
        return name
def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    query1 = 'UPDATE Players SET GamesWon = GamesWon + 1, GamesPlayed = GamesPlayed + 1 WHERE PlayerId = %s;'
    params1 = (winner,)
    query2 = 'UPDATE Players SET GamesPlayed = GamesPlayed + 1 WHERE PlayerId = %s;'
    params2 = (loser,)
    c.execute(query1, params1)
    c.execute(query2, params2)

def findPlayerToSkip():
    """Finds the player who can play the bye round.

    After finding the player, set 'PlayedByeRound' to false.

    Returns:
        PlayerID who can play the bye round.
    """
    query = 'Select (PlayedByeRound, PlayerID) From Players'
    c.execute(query)
    fetchall = c.fetchall()
    for wrappedValue in fetchall:
        value = wrappedValue[0][1:-1].split(',')
        if value[0] == 'f':
            setPlayedByeRound(value[1])
            return value[1]

def setPlayedByeRound(playerID):
    """Sets the 'PlayedByeRound' property of player with ID as PlayerID
    Args:
        playerID: ID of the player whose property needs to be set
    """
    query = 'UPDATE Players SET PlayedByeRound = TRUE WHERE PlayerId = %s'
    params = (playerID, )
    c.execute(query, params)

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    numPlayers = countPlayers()
    pairings = []
    i = 0
    playerToSkip = -1
    if numPlayers % 2 == 1:
        #Select a player who skips round
        playerToSkip = findPlayerToSkip()
    standings = playerStandings()
    while i < len(standings):
        if int(standings[i][0]) == int(playerToSkip):
            #Do not include Player i in pairing
            i = i + 1
        j = i + 1
        if int(standings[j][0]) == int(playerToSkip):
            #Do not include Player j in pairing
            j = j + 1
        pairing = (standings[i][0], standings[i][1], standings[j][0], standings[j][1])
        pairings.append(pairing)
        #Skip every other player as it is already included in the previous tuple
        i = j + 1
    return pairings

def closeDatabaseConnection():
    c.close()
    conn.close()

#Connect to server and get the cursor
conn = connect()
c = conn.cursor()
