-- 12. Оцінки студентів у певній групі з певного предмета на останньому занятті (group_id = 1, subject_id = 1)
SELECT s.name AS student_name, g.grade, g.date_received
FROM grades g
JOIN students s ON s.id = g.student_id
WHERE s.group_id = 1
  AND g.subject_id = 1
  AND g.date_received = (
      SELECT MAX(g2.date_received)
      FROM grades g2
      JOIN students s2 ON s2.id = g2.student_id
      WHERE s2.group_id = 1 AND g2.subject_id = 1
  );
