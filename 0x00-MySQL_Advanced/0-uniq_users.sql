--Script that creates TABLE Users--

CREATE TABLE IF NOT EXISTS `users`(
    `id` SERIAL NOT NULL PRIMARY KEY,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `name` VARCHAR(255)
);