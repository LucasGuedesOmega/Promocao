CREATE TABLE IF NOT EXISTS grupo_empresa(
	id_grupo_empresa serial PRIMARY KEY,
	descricao varchar(100),
	status boolean
);

CREATE TABLE IF NOT EXISTS empresa (
	id_empresa serial PRIMARY KEY,
	id_grupo_empresa bigint,
	razao_social varchar(100),
	cep char(8),
	cnpj varchar(14),
	endereco varchar(80),
	numero int, 
	bairro varchar(50),
	uf varchar(2),
	status boolean,
	token_integracao varchar(70),
	id_externo varchar(30),
	CONSTRAINT fk_grupo_empresas FOREIGN KEY (id_grupo_empresa) REFERENCES grupo_empresa(id_grupo_empresa)
);

CREATE TABLE IF NOT EXISTS historico_login(
	id_historico_login serial PRIMARY KEY,
	id_usuario bigint,
	data_ultimo_login timestamp,
	name_hardware varchar(30),
	constraint fk_usuario foreign key (id_usuario) references usuarios(id_usuario)
)

CREATE TABLE IF NOT EXISTS produtos (
	id_produto serial PRIMARY KEY, 
	id_externo varchar(30),
	descricao varchar(300),
	modalidade_produto varchar(30),
	codigo_empresa varchar(30),
	token_integracao varchar(200),
	valor double precision,
	status boolean,
	codigo_barras varchar(14),
	ncm varchar(8),
	anp varchar(10),
	id_empresa bigint,
	id_grupo_empresa bigint,
	constraint fk_empresa foreign key (id_empresa) references empresa(id_empresa),
	constraint fk_grupo_empresa foreign key (id_grupo_empresa) references grupo_empresa(id_grupo_empresa)
);

CREATE TABLE IF NOT EXISTS clientes (
	id_cliente serial PRIMARY KEY,
	nome varchar(100),
	cpf varchar(11),
	e_mail varchar(200),
	telefone varchar(20),
	status boolean,
	id_empresa bigint,
	id_grupo_empresa bigint
	constraint fk_empresa foreign key (id_empresa) references empresa(id_empresa)
	constraint fk_grupo_empresa foreign key (id_grupo_empresa) references grupo_empresa(id_grupo_empresa)
);


CREATE TABLE IF NOT EXISTS funcionario (
	id_funcionario serial PRIMARY KEY,
	nome varchar(100),
	cpf varchar(11),
	e_mail varchar(200),
	telefone varchar(20),
	status boolean,
	id_usuario bigint,
	id_empresa bigint,
	id_grupo_empresa bigint,
	constraint fk_empresa foreign key (id_empresa) references empresa(id_empresa),
	constraint fk_grupo_empresa foreign key (id_grupo_empresa) references grupo_empresa(id_grupo_empresa),
	constraint fk_usuario foreign key (id_usuario) references usuarios(id_usuario)
);

CREATE TABLE IF NOT EXISTS forma_pagamento (
	id_forma_pagamento serial PRIMARY KEY,
	id_grupo_empresa bigint,
	status boolean,
	tipo varchar(30),
	id_externo bigint,
	descricao varchar(70),
	id_empresa bigint,
	id_grupo_pagamento bigint,
	constraint fk_empresa foreign key (id_empresa) references empresa(id_empresa),
	CONSTRAINT fk_grupo_empresas FOREIGN KEY (id_grupo_empresa) REFERENCES grupo_empresa(id_grupo_empresa),
	CONSTRAINT fk_grupo_pagamento FOREIGN KEY (id_grupo_pagamento) REFERENCES grupo_pagamento(id_grupo_pagamento),
);

CREATE TABLE IF NOT EXISTS grupo_pagamento(
	id_grupo_pagamento serial PRIMARY KEY,
	descricao varchar(100),
	status boolean,
	id_empresa bigint,
	constraint fk_empresa foreign key (id_empresa) references empresa(id_empresa)
);

CREATE TABLE IF NOT EXISTS promocao(
	id_promocao serial PRIMARY KEY,
	titulo varchar(70),
	tipo varchar(25),
	desconto_total double precision,
	desconto_por_unidade double precision,
	quantidade double precision,
	id_produto bigint,
	id_grupo_empresa bigint,
	id_empresa bigint,
	data_ini timestamp,
	data_fim timestamp,
	imagem text,
	segunda boolean,
	terca boolean,
	quarta boolean,
	quinta boolean,
	sexta boolean,
	sabado boolean,
	domingo boolean,
	status boolean,
	id_grupo_pagamento bigint,
	CONSTRAINT fk_produto FOREIGN KEY (id_produto) REFERENCES produtos(id_produto),
	CONSTRAINT fk_grupo_empresa FOREIGN KEY (id_grupo_empresa) REFERENCES grupo_empresa(id_grupo_empresa),
	CONSTRAINT fk_empresa FOREIGN KEY (id_empresa) REFERENCES empresa(id_empresa),
	CONSTRAINT fk_grupo_pagamento FOREIGN KEY (id_grupo_pagamento) REFERENCES grupo_pagamento(id_grupo_pagamento)
);

CREATE TABLE IF NOT EXISTS promocao_item(
	id_promocao_item serial PRIMARY KEY,
	id_promocao bigint,
	id_produto bigint,
	minimo double precision,
	maximo double precision,
	tipo varchar(12),
	aplicar varchar(3),
	valor double precision,
	id_empresa bigint,
	constraint fk_empresa foreign key (id_empresa) references empresa(id_empresa),
	CONSTRAINT fk_promocao FOREIGN KEY (id_promocao) REFERENCES promocao(id_promocao),
	CONSTRAINT fk_produto FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
);

CREATE TABLE IF NOT EXISTS venda (
	id_venda serial PRIMARY KEY,
	id_produto bigint,
	valor double precision,
	quantidade double precision,
	codigo_empresa int,
	token_integracao varchar(100),
	data_venda date,
	hora_venda time,
	id_forma_pagamento bigint, 
	contigencia boolean,
	id_usuario bigint,
	id_promocao bigint,
	id_empresa bigint,
	link_documento_fiscal varchar(300),
	status_venda varchar(9),
	constraint fk_empresa foreign key (id_empresa) references empresa(id_empresa),
	CONSTRAINT fk_produto FOREIGN KEY (id_produto) REFERENCES produtos(id_produto),
	CONSTRAINT fk_forma_pagamento FOREIGN KEY (id_forma_pagamento) REFERENCES forma_pagamento(id_forma_pagamento),
	CONSTRAINT fk_cliente FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
	CONSTRAINT fk_promocao FOREIGN KEY (id_promocao) REFERENCES promocao(id_promocao)
);

CREATE TABLE IF NOT EXISTS produto_avulso(
	id_produto_avulso serial PRIMARY KEY,
	id_produto bigint, 
	id_grupo_empresa bigint,
	id_empresa bigint,
	id_grupo_pagamento bigint,
	valor_desconto double precision,
	valor_cash_back double precision,
	CONSTRAINT fk_produto FOREIGN KEY (id_produto) REFERENCES produtos(id_produto),
	CONSTRAINT fk_grupo_empresa FOREIGN KEY (id_grupo_empresa) REFERENCES grupo_empresa(id_grupo_empresa),
	CONSTRAINT fk_empresa FOREIGN KEY (id_empresa) REFERENCES empresa(id_empresa),
	CONSTRAINT fk_grupo_pagamento FOREIGN KEY (id_grupo_pagamento) REFERENCES grupo_pagamento(id_grupo_pagamento)
);

CREATE TABLE IF NOT EXISTS voucher (
	id_voucher serial PRIMARY KEY,
	codigo_voucher varchar(30),
	id_usuario bigint,
	data_ini timestamp,
	status boolean,
	id_empresa bigint,
	id_promocao bigint,
	tipoCodigo varchar(10),
	constraint fk_empresa foreign key (id_empresa) references empresa(id_empresa),
	CONSTRAINT fk_usuario FOREIGN KEY(id_usuario)  REFERENCES usuarios(id_usuario),
	CONSTRAINT fk_promocao FOREIGN KEY(id_promocao)  REFERENCES promocao(id_promocao)
)

CREATE TABLE IF NOT EXISTS promocao_empresas (
	id_promocao_empresa serial PRIMARY KEY,
	id_promocao bigint,
	id_empresa bigint,
	id_grupo_empresa bigint,
	status boolean,
	constraint fk_empresa foreign key (id_empresa) references empresa(id_empresa),
	CONSTRAINT fk_promocao FOREIGN KEY(id_promocao)  REFERENCES promocao(id_promocao),
	CONSTRAINT fk_grupo_empresa FOREIGN KEY(id_grupo_empresa)  REFERENCES grupo_empresa(id_grupo_empresa)
)

CREATE TABLE IF NOT EXISTS total_valores_clientes (
	id_total_valores_clientes serial PRIMARY KEY,
	id_cliente bigint,
	valor double precision,
	tipo varchar(3),
	constraint fk_cliente foreign key (id_cliente) references clientes(id_cliente)
);

CREATE TABLE IF NOT EXISTS historico_promocao (
	id_historico serial PRIMARY KEY,
	id_cliente bigint,
	valor double precision,
	valor_total_venda double precision,
	data_emissao timestamp,
	constraint fk_cliente foreign key (id_cliente) references clientes(id_cliente)
)

CREATE TABLE IF NOT EXISTS confirma_email (
	id_confirma_email serial PRIMARY KEY,
	id_usuario bigint,
	codigo varchar(7),
	data timestamp,
	CONSTRAINT fk_usuario FOREIGN KEY(id_usuario)  REFERENCES usuarios(id_usuario)
)

CREATE TABLE IF NOT EXISTS usuarios (
	id_usuario serial PRIMARY KEY,
	username VARCHAR(200),
	senha varchar(200),
	e_mail varchar(200),
	status boolean,
	user_admin boolean,
	user_app boolean,
	admin_posto boolean,
	id_empresa bigint,
	id_grupo_empresa bigint,
	id_grupo_usuario bigint,
	constraint fk_grupo_empresa foreign key (id_grupo_empresa) references grupo_empresa(id_grupo_empresa)
	constraint fk_grupo_usuario foreign key (id_grupo_usuario) references grupo_usuario(id_grupo_usuario)
	constraint fk_empresa foreign key (id_empresa) references empresa(id_empresa)
);

CREATE TABLE IF NOT EXISTS grupo_usuario (
	id_grupo_usuario serial PRIMARY KEY,
	nome varchar(50),
	id_permissao bigint,
	status boolean,
	CONSTRAINT fk_permissao FOREIGN KEY(id_permissao)  REFERENCES permissao(id_permissao)
)

CREATE TABLE IF NOT EXISTS permissao (
	id_permissao serial PRIMARY KEY,
	nome varchar(50)
)

CREATE TABLE IF NOT EXISTS permissao_tela_acao (
	id_permissao_tela_acao serial PRIMARY KEY,
	id_permissao bigint,
	id_tela_acao bigint,
	CONSTRAINT fk_permissao FOREIGN KEY(id_permissao)  REFERENCES permissao(id_permissao)
	CONSTRAINT fk_tela_acao FOREIGN KEY(id_tela_acao)  REFERENCES tela(id_tela_acao)
)

CREATE TABLE IF NOT EXISTS tela_acao (
	id_tela_acao serial PRIMARY KEY,
	nome varchar(50)
)

-- INSERIR TELAS
INSERT INTO tela_acao(nome) values ('DASHBOARD');
INSERT INTO tela_acao(nome) values ('CLIENTE');
INSERT INTO tela_acao(nome) values ('PRODUTO');
INSERT INTO tela_acao(nome) values ('PROMOCAO');
INSERT INTO tela_acao(nome) values ('GRUPO_PAGAMENTO');
INSERT INTO tela_acao(nome) values ('GRUPO_EMPRESA');
INSERT INTO tela_acao(nome) values ('SUPER_USUARIO');
INSERT INTO tela_acao(nome) values ('GRUPO_USUARIO');
INSERT INTO tela_acao(nome) values ('INSERT');
INSERT INTO tela_acao(nome) values ('UPDATE');
