-- 5. Знайти які курси читає певний викладач
SELECT sub.name AS subject_name
FROM subjects sub
WHERE sub.teacher_id = (SELECT id FROM teachers LIMIT 1);
