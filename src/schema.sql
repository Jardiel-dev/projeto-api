-- Limpa tabelas antigas
DROP TABLE IF EXISTS artilheiros CASCADE;
DROP TABLE IF EXISTS tabela_partidas_tratada CASCADE;
DROP TABLE IF EXISTS jogadores CASCADE;
DROP TABLE IF EXISTS tecnicos CASCADE;
DROP TABLE IF EXISTS arbitros CASCADE;
DROP TABLE IF EXISTS temporadas CASCADE;
DROP TABLE IF EXISTS competicoes CASCADE;
DROP TABLE IF EXISTS times CASCADE;

-- 1. Competicoes
CREATE TABLE IF NOT EXISTS competicoes (
    id_competicao INT PRIMARY KEY,
    id_area INT,
    nome_competicao VARCHAR(100) NOT NULL,
    codigo_competicao VARCHAR(20),
    tipo VARCHAR(50)
);

-- 2. Temporadas
CREATE TABLE IF NOT EXISTS temporadas (
    id_temporada INT PRIMARY KEY,
    id_competicao INT,
    ano_inicio INT,
    ano_fim INT,
    data_inicio_completa TIMESTAMP,
    data_fim_completa TIMESTAMP,
    FOREIGN KEY (id_competicao) REFERENCES competicoes(id_competicao)
);

-- 3. Times
CREATE TABLE IF NOT EXISTS times (
    id_time INT PRIMARY KEY,
    nome_time VARCHAR(100) NOT NULL,
    sigla VARCHAR(10),
    fundacao INT,
    estadio VARCHAR(100)
);

-- 4. Tecnicos
CREATE TABLE IF NOT EXISTS tecnicos (
    id_tecnico INT PRIMARY KEY,
    id_time INT,
    nome_tecnico VARCHAR(100) NOT NULL,
    nacionalidade VARCHAR(50),
    data_nascimento TIMESTAMP,
    FOREIGN KEY (id_time) REFERENCES times(id_time)
);

-- 5. Jogadores
CREATE TABLE IF NOT EXISTS jogadores (
    id_jogador INT PRIMARY KEY,
    id_time INT,
    nome_jogador VARCHAR(100) NOT NULL,
    posicao VARCHAR(50),
    nacionalidade VARCHAR(50),
    data_nascimento TIMESTAMP,
    FOREIGN KEY (id_time) REFERENCES times(id_time)
);

-- 6. Arbitros
CREATE TABLE IF NOT EXISTS arbitros (
    id_arbitro INT PRIMARY KEY,
    nome_arbitro VARCHAR(100) NOT NULL,
    nacionalidade VARCHAR(50),
    tipo VARCHAR(50)
);

-- 7. Partidas (tabela_partidas_tratada)
CREATE TABLE IF NOT EXISTS tabela_partidas_tratada (
    id_partida INT PRIMARY KEY,
    id_competicao INT,
    id_temporada INT,
    id_area INT,
    id_casa INT,
    id_fora INT,
    id_arbitro INT,
    data_partida TIMESTAMP,
    status VARCHAR(20),
    rodada INT,
    resultado VARCHAR(20),
    placar_casa_intervalo INT,  -- <--- ADICIONADA
    placar_casa_final INT,
    placar_fora_intervalo INT,  -- <--- ADICIONADA
    placar_fora_final INT,
    FOREIGN KEY (id_competicao) REFERENCES competicoes(id_competicao),
    FOREIGN KEY (id_temporada) REFERENCES temporadas(id_temporada),
    FOREIGN KEY (id_casa) REFERENCES times(id_time),
    FOREIGN KEY (id_fora) REFERENCES times(id_time),
    FOREIGN KEY (id_arbitro) REFERENCES arbitros(id_arbitro)
);

-- 8. Artilheiros
CREATE TABLE IF NOT EXISTS artilheiros (
    id_jogador INT,
    id_time INT,
    gols INT,
    assistencias INT,
    penaltis INT,
    PRIMARY KEY (id_jogador, id_time),
    FOREIGN KEY (id_jogador) REFERENCES jogadores(id_jogador),
    FOREIGN KEY (id_time) REFERENCES times(id_time)
);