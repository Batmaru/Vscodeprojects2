CREATE TABLE venduti (
    id SERIAL PRIMARY KEY,               -- ID univoco per ogni vendita
    filiale_id INT NOT NULL,             -- ID della filiale
    tipo VARCHAR(20) NOT NULL,           -- Tipo di veicolo ('automobile' o 'motocicletta')
    item_id INT NOT NULL,                -- ID del veicolo venduto
    data_vendita DATE NOT NULL,          -- Data della vendita
    CONSTRAINT fk_filiale FOREIGN KEY (filiale_id) REFERENCES filiali(id),
    CONSTRAINT chk_tipo CHECK (tipo IN ('automobile', 'motocicletta'))
);
