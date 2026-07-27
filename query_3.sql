-- 3. Знайти середній бал у групах з певного предмета
SELECT gr.name AS group_name, ROUND(AVG(g.grade), 2) AS average_grade
FROM groups gr
JOIN students s ON gr.id = s.group_id
JOIN grades g ON s.id = g.student_id
WHERE g.subject_id = (SELECT id FROM subjects LIMIT 1)
GROUP BY gr.id, gr.name;
