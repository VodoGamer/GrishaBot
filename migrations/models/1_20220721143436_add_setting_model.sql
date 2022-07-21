-- upgrade --
CREATE TABLE IF NOT EXISTS "setting" (
    "id" INT NOT NULL  PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL,
    "value" INT NOT NULL,
    "chat_id" INT NOT NULL REFERENCES "chat" ("id") ON DELETE CASCADE
);
-- downgrade --
DROP TABLE IF EXISTS "setting";
