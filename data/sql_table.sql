<<<<<<< HEAD
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
=======
TABLE "history" (
	"id"	INTEGER,
	"date"	TEXT NOT NULL,
	"time"	TEXT NOT NULL,
	"amount_from"	REAL NOT NULL,
	"crypto_from"	TEXT NOT NULL,
	"amount_to"	REAL NOT NULL,
	"crypto_to"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)
>>>>>>> e4a7933771f54aca0f168df6dece23cfef34130e
