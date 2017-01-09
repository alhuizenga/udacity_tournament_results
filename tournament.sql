-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE player (
    id serial PRIMARY KEY,
    name text);

CREATE TABLE match (
    id serial PRIMARY KEY,
    winner int REFERENCES player (id),
    loser int REFERENCES player (id));

CREATE VIEW wins AS
SELECT player.id, player.name, COUNT(match.winner) AS wins
FROM player LEFT JOIN match
ON player.id = match.winner
GROUP BY player.id, player.name
ORDER BY wins DESC;

CREATE VIEW matches AS
SELECT player.id, player.name, COUNT(match.id) AS matches
FROM player
LEFT JOIN match ON (match.winner = player.id OR match.loser = player.id)
GROUP BY player.id, player.name
ORDER BY matches DESC;

CREATE VIEW standings AS
SELECT player.id, player.name, wins.wins, matches.matches
FROM player
LEFT JOIN wins ON player.id = wins.id
LEFT JOIN matches ON player.id = matches.id
GROUP BY player.id, player.name, wins.wins, matches.matches
ORDER BY wins DESC;
