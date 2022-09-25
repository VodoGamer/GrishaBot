-- upgrade --
CREATE TABLE IF NOT EXISTS "chat" (
    "id" INT NOT NULL  PRIMARY KEY,
    "messages_count" INT NOT NULL  DEFAULT 0,
    "last_person_of_day" TIMESTAMPTZ,
    "last_casino" TIMESTAMPTZ
);
CREATE TABLE IF NOT EXISTS "casino" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "winner_feature" VARCHAR(5) NOT NULL,
    "chat_id" INT NOT NULL REFERENCES "chat" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "casino"."winner_feature" IS 'RED: 🔴\nBLACK: ⚫️\nGREEN: 🍀';
CREATE TABLE IF NOT EXISTS "setting" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "cid" INT NOT NULL,
    "value" INT NOT NULL,
    "chat_id" INT NOT NULL REFERENCES "chat" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "uid" INT NOT NULL,
    "is_admin" BOOL NOT NULL  DEFAULT False,
    "is_owner" BOOL NOT NULL  DEFAULT False,
    "custom_name" VARCHAR(255),
    "messages_count" INT NOT NULL  DEFAULT 0,
    "sex_request" INT,
    "money" INT NOT NULL  DEFAULT 0,
    "last_bonus_use" TIMESTAMPTZ,
    "dick_size" INT NOT NULL  DEFAULT 0,
    "last_dick_growth_use" TIMESTAMPTZ,
    "casino_bet_amount" INT,
    "casino_bet_color" VARCHAR(5),
    "last_coin_game" TIMESTAMPTZ,
    "chat_id" INT NOT NULL REFERENCES "chat" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "user"."casino_bet_color" IS 'RED: 🔴\nBLACK: ⚫️\nGREEN: 🍀';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
