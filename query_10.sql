-- 10. Список курсів, які певному студенту читає певний викладач (student_id = 1, teacher_id = 1)
SELECT DISTINCT sub.name AS subject_name
FROM subjects sub
JOIN grades g ON sub.id = g.subject_id
JOIN students s ON s.id = g.student_id
WHERE s.id = 1 AND sub.teacher_id = 1;
