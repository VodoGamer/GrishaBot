-- upgrade --
ALTER TABLE "chat" ADD "last_shop_message_id" INT;
-- downgrade --
ALTER TABLE "chat" DROP COLUMN "last_shop_message_id";
