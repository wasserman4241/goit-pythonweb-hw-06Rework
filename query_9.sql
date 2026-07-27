-- 9. Знайти список курсів, які відвідує студент
SELECT DISTINCT sub.name AS subject_name
FROM subjects sub
JOIN grades g ON sub.id = g.subject_id
WHERE g.student_id = (SELECT id FROM students LIMIT 1);
