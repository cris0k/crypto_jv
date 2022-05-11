CREATE TABLE "history" (
	"id"	INTEGER,
	"date"	TEXT NOT NULL,
	"time"	TEXT NOT NULL,
	"crypto_from"	TEXT NOT NULL,
	"amount_from"	REAL NOT NULL,
	"crypto_to"	TEXT NOT NULL,
	"amount_to"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);