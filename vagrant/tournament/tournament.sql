-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament
CREATE TABLE Players(
  PlayerID SERIAL PRIMARY KEY,
  PlayerName VARCHAR(255),
  GamesPlayed INT DEFAULT 0,
  GamesWon INT DEFAULT 0,
  PlayedByeRound BOOLEAN DEFAULT FALSE
);

CREATE TABLE Matches(
  PlayerA INT REFERENCES Players(PlayerID),
  PlayerB INT REFERENCES Players(PlayerID),
  Winner INT REFERENCES Players(PlayerID),
  PRIMARY KEY(PlayerA, PlayerB),
  CHECK(PlayerA <> PlayerB)
);
