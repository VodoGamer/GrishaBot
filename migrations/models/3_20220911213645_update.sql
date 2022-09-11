-- upgrade --
ALTER TABLE "setting" DROP COLUMN "type";
-- downgrade --
ALTER TABLE "setting" ADD "type" SMALLINT NOT NULL;
