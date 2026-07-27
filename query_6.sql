-- 6. Знайти список студентів у певній групі
SELECT s.id, s.name
FROM students s
WHERE s.group_id = (SELECT id FROM groups LIMIT 1);
