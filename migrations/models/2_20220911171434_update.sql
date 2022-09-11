-- upgrade --
ALTER TABLE "chat" ADD "last_person_of_day" TIMESTAMPTZ;
ALTER TABLE "chat" ADD "last_casino" TIMESTAMPTZ;
DROP TABLE IF EXISTS "chat_cooldown";
-- downgrade --
ALTER TABLE "chat" DROP COLUMN "last_person_of_day";
ALTER TABLE "chat" DROP COLUMN "last_casino";
