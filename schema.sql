
-- Tabla Fibras
CREATE TABLE IF NOT EXISTS fibras (
    id_fibra INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE
);

-- Tabla Velas
CREATE TABLE IF NOT EXISTS velas (
    id_vela INTEGER PRIMARY KEY AUTOINCREMENT,
    id_fibra INTEGER NOT NULL,
    timestamp  INTEGER NOT NULL,
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    close REAL NOT NULL,
    volume REAL NOT NULL,
    frecuencia TEXT NOT NULL,
    FOREIGN KEY (id_fibra) REFERENCES fibras(id_fibra),
    UNIQUE (id_fibra,frecuencia,timestamp)
);

-- Tabla Distribuciones
CREATE TABLE IF NOT EXISTS distribuciones (
    id_distribucion INTEGER PRIMARY KEY AUTOINCREMENT,
    id_fibra INTEGER NOT NULL,
    fecha_ex_dividendo TEXT NOT NULL,
    fecha_pago TEXT NOT NULL,
    tipo_dividendo TEXT NOT NULL,
    dividendo REAL NOT NULL,
    rendimiento REAL NOT NULL,
    FOREIGN KEY (id_fibra) REFERENCES fibras(id_fibra),
    UNIQUE (id_fibra,fecha_ex_dividendo,fecha_pago)
);
