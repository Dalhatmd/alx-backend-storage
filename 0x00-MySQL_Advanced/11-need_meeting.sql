-- creates a view
CREATE OR REPLACE VIEW need_meeting AS
SELECT name
FROM students
WHERE score < 80
  AND (last_meeting IS NULL OR last_meeting < CURRENT_DATE - INTERVAL '1 month');

