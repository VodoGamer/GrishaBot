-- upgrade --
ALTER TABLE "chat_cooldown" ALTER COLUMN "person_of_day" DROP NOT NULL;
ALTER TABLE "chat_cooldown" ALTER COLUMN "casino" DROP NOT NULL;
-- downgrade --
ALTER TABLE "chat_cooldown" ALTER COLUMN "person_of_day" SET NOT NULL;
ALTER TABLE "chat_cooldown" ALTER COLUMN "casino" SET NOT NULL;
