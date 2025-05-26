CREATE TABLE IF NOT EXISTS `user` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


INSERT INTO users (username, email ) VALUES
    ('arsh', 'arsh@gmail.com'),
    ('jack', 'jack@gmail.com');INSERT INTO medical_history (
        history_id,
        patient_id,
        entry_date,
        diagnosis,
        treatment,
        notes,
        severity
      )
    VALUES (
        history_id:intINSERT INTO appointments (
            appointment_id,
            patient_id,
            appointment_date,
            start_time,
            end_time,
            purpose,
            status,
            notes
          )
        VALUES (
            appointment_id:int,
            patient_id:int,
            'appointment_date:date',
            'start_time:time',
            'end_time:time',
            'purpose:varchar',
            'status:enum',
            'notes:text'
          );,
        patient_id:int,
        'entry_date:date',
        'diagnosis:varchar',
        'treatment:text',
        'notes:text',
        severity:int
      );