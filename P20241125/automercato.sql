-- Tabella filiali
CREATE TABLE filiali (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

-- Tabella automobili
CREATE TABLE automobili (
    id SERIAL PRIMARY KEY,
    modello VARCHAR(255) NOT NULL,
    marca VARCHAR(255) NOT NULL,
    anno INT NOT NULL,
    disponibilita BOOLEAN NOT NULL DEFAULT TRUE,
    filiale_id INT REFERENCES filiali(id)
);

-- Tabella motociclette
CREATE TABLE motociclette (
    id SERIAL PRIMARY KEY,
    modello VARCHAR(255) NOT NULL,
    marca VARCHAR(255) NOT NULL,
    anno INT NOT NULL,
    disponibilita BOOLEAN NOT NULL DEFAULT TRUE,
    filiale_id INT REFERENCES filiali(id)
);


CREATE TABLE utenti (
    id serial PRIMARY KEY,       -- Identificativo univoco per ogni utente
    username VARCHAR(50) NOT NULL UNIQUE,    -- Nome utente univoco
    password VARCHAR(255) NOT NULL,          -- Password (si consiglia di salvare gli hash, non la password in chiaro)
    nome VARCHAR(50) NOT NULL,               -- Nome dell'utente
    cognome VARCHAR(50) NOT NULL,            -- Cognome dell'utente
    email VARCHAR(100) UNIQUE,               -- Email (opzionale, ma utile per il recupero password)
);


-- Tabella venduti
CREATE TABLE venduti (
    id SERIAL PRIMARY KEY,
    filiale_id INT REFERENCES filiali(id),
    veicolo_id INT NOT NULL,
    tipo VARCHAR(50) CHECK (tipo IN ('automobile', 'motocicletta')),
    data_vendita DATE NOT NULL
);

-- Dati per la tabella filiali
INSERT INTO filiali (nome) VALUES
('Filiale Roma'),
('Filiale Milano'),
('Filiale Napoli');

-- Dati per la tabella automobili
INSERT INTO automobili (modello, marca, anno, disponibilita, filiale_id) VALUES
('Panda', 'Fiat', 2020, TRUE, 1),
('Golf', 'Volkswagen', 2018, TRUE, 2),
('Focus', 'Ford', 2019, FALSE, 3);

-- Dati per la tabella motociclette
INSERT INTO motociclette (modello, marca, anno, disponibilita, filiale_id) VALUES
('Monster', 'Ducati', 2021, TRUE, 1),
('R1', 'Yamaha', 2020, FALSE, 2),
('CBR', 'Honda', 2022, TRUE, 3);

-- Dati per la tabella venduti
INSERT INTO venduti (filiale_id, veicolo_id, tipo, data_vendita) VALUES
(1, 1, 'automobile', '2023-05-01'),
(2, 2, 'automobile', '2023-06-15'),
(3, 1, 'motocicletta', '2023-07-10'),
(2, 2, 'motocicletta', '2023-08-20');

INSERT INTO utenti (username, password, nome, cognome, email)
VALUES 
    ('admin', 'hashed_password1', 'Mario', 'Rossi', 'mario.rossi@example.com'),
    ('user1', 'hashed_password2', 'Luigi', 'Bianchi', 'luigi.bianchi@example.com'),
    ('user2', 'hashed_password3', 'Giulia', 'Verdi', 'giulia.verdi@example.com');
