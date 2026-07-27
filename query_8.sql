-- 8. Знайти середній бал, який ставить певний викладач зі своїх предметів
SELECT t.name AS teacher_name, ROUND(AVG(g.grade), 2) AS average_grade
FROM teachers t
JOIN subjects sub ON t.id = sub.teacher_id
JOIN grades g ON sub.id = g.subject_id
WHERE t.id = (SELECT id FROM teachers LIMIT 1)
GROUP BY t.id, t.name;
