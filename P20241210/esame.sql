-- Tabella delle filiali
CREATE TABLE filiali (
    partita_iva VARCHAR(100) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    indirizzo_sede VARCHAR(255) NOT NULL,
    civico INT NOT NULL,
    telefono VARCHAR(20) NOT NULL
);

-- Tabella delle case in vendita
CREATE TABLE case_in_vendita (
    catastale VARCHAR(50) PRIMARY KEY,
    indirizzo VARCHAR(255) NOT NULL,
    numero_civico INT NOT NULL,
    piano INT,
    metri FLOAT NOT NULL,
    vani INT NOT NULL,
    prezzo DECIMAL(15, 2) NOT NULL,
    stato ENUM('LIBERO', 'OCCUPATO') NOT NULL,
    filiale_proponente VARCHAR(16) NOT NULL,
    FOREIGN KEY (filiale_proponente) REFERENCES filiali(partita_iva)
);

-- Tabella delle case in affitto
CREATE TABLE case_in_affitto (
    catastale VARCHAR(50) PRIMARY KEY,
    indirizzo VARCHAR(255) NOT NULL,
    civico INT NOT NULL,
    tipo_affitto ENUM('PARZIALE', 'TOTALE') NOT NULL,
    bagno_personale BOOLEAN NOT NULL,
    prezzo_mensile DECIMAL(15, 2) NOT NULL,
    filiale_proponente VARCHAR(16) NOT NULL,
    FOREIGN KEY (filiale_proponente) REFERENCES filiali(partita_iva)
);

-- Tabella delle vendite di case
CREATE TABLE vendite_casa (
    catastale VARCHAR(50),
    data_vendita DATE NOT NULL,
    filiale_proponente VARCHAR(16) NOT NULL,
    filiale_venditrice VARCHAR(16) NOT NULL,
    prezzo_vendita DECIMAL(15, 2) NOT NULL,
    PRIMARY KEY (catastale, data_vendita),
    FOREIGN KEY (catastale) REFERENCES case_in_vendita(catastale),
    FOREIGN KEY (filiale_proponente) REFERENCES filiali(partita_iva),
    FOREIGN KEY (filiale_venditrice) REFERENCES filiali(partita_iva)
);

-- Tabella degli affitti di case
CREATE TABLE affitti_casa (
    catastale VARCHAR(50),
    data_affitto DATE NOT NULL,
    filiale_proponente VARCHAR(16) NOT NULL,
    filiale_venditrice VARCHAR(16) NOT NULL,
    prezzo_affitto DECIMAL(15, 2) NOT NULL,
    durata_contratto INT NOT NULL, -- Durata in mesi
    PRIMARY KEY (catastale, data_affitto),
    FOREIGN KEY (catastale) REFERENCES case_in_affitto(catastale),
    FOREIGN KEY (filiale_proponente) REFERENCES filiali(partita_iva),
    FOREIGN KEY (filiale_venditrice) REFERENCES filiali(partita_iva)
);


INSERT INTO filiali VALUES
('1234567890123456', 'Filiale Centro', 'Via Roma', 10, '051123456'),
('2234567890123456', 'Filiale Nord', 'Via Milano', 25, '051223456'),
('3234567890123456', 'Filiale Sud', 'Via Napoli', 5, '051323456'),
('4234567890123456', 'Filiale Est', 'Via Firenze', 15, '051423456'),
('5234567890123456', 'Filiale Ovest', 'Via Torino', 30, '051523456');

INSERT INTO case_in_vendita VALUES
('A001', 'Via Verdi', 3, 1, 80.0, 3, 120000.00, 'LIBERO', '1234567890123456'),
('A002', 'Via Bianchi', 5, 2, 60.0, 2, 100000.00, 'OCCUPATO', '1234567890123456'),
('A003', 'Via Rossi', 8, 0, 50.0, 2, 95000.00, 'LIBERO', '2234567890123456'),
('A004', 'Via Gialli', 10, 3, 120.0, 4, 200000.00, 'OCCUPATO', '2234567890123456'),
('A005', 'Via Azzurri', 12, 2, 70.0, 3, 130000.00, 'LIBERO', '3234567890123456');

INSERT INTO case_in_affitto VALUES
('B001', 'Via Verdi', 3, 'PARZIALE', TRUE, 500.00, '1234567890123456'),
('B002', 'Via Bianchi', 5, 'TOTALE', FALSE, 700.00, '1234567890123456'),
('B003', 'Via Rossi', 8, 'TOTALE', TRUE, 800.00, '2234567890123456'),
('B004', 'Via Gialli', 10, 'PARZIALE', FALSE, 600.00, '2234567890123456'),
('B005', 'Via Azzurri', 12, 'TOTALE', TRUE, 750.00, '3234567890123456');


INSERT INTO vendite_casa VALUES
('A001', '2023-01-15', '1234567890123456', '1234567890123456', 115000.00),
('A002', '2023-02-10', '1234567890123456', '2234567890123456', 95000.00),
('A003', '2023-03-20', '2234567890123456', '3234567890123456', 90000.00),
('A004', '2023-04-25', '2234567890123456', '1234567890123456', 190000.00),
('A005', '2023-05-30', '3234567890123456', '3234567890123456', 125000.00);


INSERT INTO affitti_casa VALUES
('B001', '2023-06-15', '1234567890123456', '1234567890123456', 500.00, 12),
('B002', '2023-07-01', '1234567890123456', '2234567890123456', 700.00, 6),
('B003', '2023-08-10', '2234567890123456', '3234567890123456', 800.00, 24),
('B004', '2023-09-05', '2234567890123456', '1234567890123456', 600.00, 18),
('B005', '2023-10-25', '3234567890123456', '3234567890123456', 750.00, 12);
