#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""

    DB = connect()
    cur = DB.cursor()
    query = ("DELETE FROM match;")
    cur.execute(query)
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""

    DB = connect()
    cur = DB.cursor()
    query = ("DELETE FROM player;")
    cur.execute(query)
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    cur = DB.cursor()
    query = ("SELECT COUNT(*) FROM player;")
    cur.execute(query)
    c = cur.fetchone()[0]
    DB.close()
    return c


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    cur = DB.cursor()
    query = ("INSERT INTO player (name) VALUES (%s);")
    parameter = (bleach.clean(name),)
    cur.execute(query, parameter)
    DB.commit()
    DB.close()


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

    DB = connect()
    cur = DB.cursor()
    query = "SELECT * FROM standings;"
    cur.execute(query)
    standings = cur.fetchall()
    DB.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    DB = connect()
    cur = DB.cursor()
    query = ("INSERT INTO match (winner, loser) VALUES (%s, %s);")
    parameter = (bleach.clean(winner), bleach.clean(loser))
    cur.execute(query, parameter)
    DB.commit()
    DB.close()


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

    standings = playerStandings()

    listA = []
    for row in standings[::2]:
        x = (row[0], row[1])
        listA.append(x)

    listB = []
    for row in standings[1::2]:
        y = (row[0], row[1])
        listB.append(y)

    pairings = []
    l = len(listA)
    for x in range (0, l):
        z = (listA[x][0], listA[x][1], listB[x][0], listB[x][1])
        pairings.append(z)

    return pairings
