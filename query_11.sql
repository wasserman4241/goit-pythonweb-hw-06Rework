-- 11. Середній бал, який певний викладач ставить певному студентові (teacher_id = 1, student_id = 1)
SELECT s.name AS student_name, t.name AS teacher_name, ROUND(AVG(g.grade), 2) AS average_grade
FROM grades g
JOIN students s ON s.id = g.student_id
JOIN subjects sub ON sub.id = g.subject_id
JOIN teachers t ON t.id = sub.teacher_id
WHERE t.id = 1 AND s.id = 1
GROUP BY s.id, s.name, t.id, t.name;
