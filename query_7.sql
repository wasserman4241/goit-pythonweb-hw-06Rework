-- 7. Знайти оцінки студентів у окремій групі з певного предмета
SELECT s.name AS student_name, g.grade, g.date_received
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE s.group_id = (SELECT id FROM groups LIMIT 1)
  AND g.subject_id = (SELECT id FROM subjects LIMIT 1);
