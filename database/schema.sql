-- 1. Удаляем таблицы, если они вдруг остались от старых попыток
-- Это нужно, чтобы при каждом запуске "стройки" база была чистой
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS masters;
DROP TABLE IF EXISTS clients;

-- 2. Таблица клиентов
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    name VARCHAR(100),
    phone VARCHAR(20)
);

-- 3. Таблица мастеров
CREATE TABLE masters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100)
);

-- 4. Таблица записей
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE,
    master_id INTEGER REFERENCES masters(id) ON DELETE CASCADE,
    appointment_date TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'pending'
);