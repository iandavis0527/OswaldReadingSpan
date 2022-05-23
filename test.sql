CREATE TEMPORARY TABLE tmp AS
SELECT *
FROM ReadingSpanResult;
UPDATE tmp
SET id = 2;
UPDATE tmp
SET subject_id = "101";
INSERT INTO ReadingSpanResult
SELECT *
FROM tmp;
DROP TABLE tmp;
CREATE TEMPORARY TABLE tmp AS
SELECT *
FROM ReadingSpanLetterResponse;
UPDATE tmp
SET id = NULL;
UPDATE tmp
SET test_id = 2;
INSERT INTO ReadingSpanLetterResponse
SELECT *
FROM tmp;
DROP TABLE tmp;
CREATE TEMPORARY TABLE tmp AS
SELECT *
FROM ReadingSpanSentenceResponse;
UPDATE tmp
SET id = NULL;
UPDATE tmp
SET test_id = 2;
INSERT INTO ReadingSpanSentenceResponse
SELECT *
FROM tmp;
DROP TABLE tmp;