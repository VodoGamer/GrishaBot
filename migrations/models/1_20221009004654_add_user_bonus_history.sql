-- upgrade --
ALTER TABLE "user" DROP COLUMN "last_bonus_use";
CREATE TABLE IF NOT EXISTS "user_bonus" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "bonus_value" INT NOT NULL,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);-- downgrade --
ALTER TABLE "user" ADD "last_bonus_use" TIMESTAMPTZ;
DROP TABLE IF EXISTS "user_bonus";
