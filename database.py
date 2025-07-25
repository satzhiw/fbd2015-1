from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, DateTime, Text, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime


DATABASE_URL = "postgresql://app_user:07102004Will@localhost:5432/sistema_acompanhamento"

engine = create_engine(DATABASE_URL, echo=False)


Base = declarative_base()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Pessoa(Base):
    __tablename__ = "pessoa" # Nome da tabela no banco de dados

    id_pessoa = Column(Integer, primary_key=True, index=True) # Coluna de chave primária
    nome_completo = Column(String(255), nullable=False)
    data_nasc = Column(Date)
    cpf = Column(String(14), unique=True, nullable=False)
    rg = Column(String(20), unique=True)
    genero = Column(String(50))
    email = Column(String(255), unique=True, nullable=False)
    telefone = Column(String(20))

    membros = relationship("MembroDaFamilia", back_populates="pessoa")
    profissionais = relationship("Profissional", back_populates="pessoa")
    usuarios = relationship("Usuario", back_populates="pessoa")
    atendimentos_membro = relationship("Atendimento", back_populates="pessoa_membro")
    beneficios_membro = relationship("Beneficio", back_populates="pessoa_membro")

    def __repr__(self):
        return f"<Pessoa(id={self.id_pessoa}, nome='{self.nome_completo}')>"

class Familia(Base):
    __tablename__ = "familia"

    id_familia = Column(Integer, primary_key=True, index=True)
    nome_familia = Column(String(255), nullable=False)
    endereco = Column(String(255), nullable=False)
    bairro = Column(String(100))
    cidade = Column(String(100))
    estado = Column(String(50))
    cep = Column(String(10), nullable=False)
    telefone = Column(String(20), nullable=False)
    renda_mensal = Column(Numeric(10, 2))
    data_cadastro = Column(Date, default=datetime.now().date(), nullable=False)
    status_vulnerabilidade = Column(Boolean, nullable=False)
    observacoes = Column(Text)

    # Relacionamentos
    membros = relationship("MembroDaFamilia", back_populates="familia")
    atendimentos = relationship("Atendimento", back_populates="familia")
    beneficios = relationship("Beneficio", back_populates="familia")
    necessidades = relationship("Necessidade", back_populates="familia")
    ocorrencias = relationship("Ocorrencia", back_populates="familia")

    def __repr__(self):
        return f"<Familia(id={self.id_familia}, nome='{self.nome_familia}')>"

class MembroDaFamilia(Base):
    __tablename__ = "membro_da_familia"

    id_membro_familia = Column(Integer, primary_key=True, index=True)
    id_pessoa = Column(Integer, ForeignKey("pessoa.id_pessoa"), nullable=False)
    id_familia = Column(Integer, ForeignKey("familia.id_familia"), nullable=False)
    parentesco = Column(String(50), nullable=False)
    escolaridade = Column(String(100))
    ocupacao = Column(String(100))
    situacao_saude = Column(Text)
    beneficios = Column(Text) 

    # Relacionamentos
    pessoa = relationship("Pessoa", back_populates="membros")
    familia = relationship("Familia", back_populates="membros")

    def __repr__(self):
        return f"<Membro(id={self.id_membro_familia}, pessoa_id={self.id_pessoa}, familia_id={self.id_familia})>"

class Profissional(Base):
    __tablename__ = "profissional"

    id_profissional = Column(Integer, ForeignKey("pessoa.id_pessoa"), primary_key=True)
    cargo = Column(String(100), nullable=False)
    setor = Column(String(100), nullable=False)

    # Relacionamento
    pessoa = relationship("Pessoa", back_populates="profissionais")
    atendimentos = relationship("Atendimento", back_populates="profissional")
    ocorrencias = relationship("Ocorrencia", back_populates="profissional")

    def __repr__(self):
        return f"<Profissional(id={self.id_profissional}, cargo='{self.cargo}')>"

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, ForeignKey("pessoa.id_pessoa"), primary_key=True)
    nome_usuario = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    data_criacao = Column(Date, default=datetime.now().date(), nullable=False)
    status_conta = Column(String(50), nullable=False)
    ultimo_login = Column(DateTime)

    # Relacionamento
    pessoa = relationship("Pessoa", back_populates="usuarios")
    perfis = relationship("UsuarioPerfil", back_populates="usuario")

    def __repr__(self):
        return f"<Usuario(id={self.id_usuario}, nome_usuario='{self.nome_usuario}')>"

class Perfil(Base):
    __tablename__ = "perfil"

    id_perfil = Column(Integer, primary_key=True, index=True)
    nome_perfil = Column(String(100), unique=True, nullable=False)
    descricao_perfil = Column(Text)

    # Relacionamentos
    usuarios = relationship("UsuarioPerfil", back_populates="perfil")
    permissoes = relationship("PerfilPermissao", back_populates="perfil")

    def __repr__(self):
        return f"<Perfil(id={self.id_perfil}, nome='{self.nome_perfil}')>"

class Permissao(Base):
    __tablename__ = "permissao"

    id_permissao = Column(Integer, primary_key=True, index=True)
    nome_permissao = Column(String(100), unique=True, nullable=False)
    descricao_permissao = Column(Text)

    # Relacionamento
    perfis = relationship("PerfilPermissao", back_populates="permissao")

    def __repr__(self):
        return f"<Permissao(id={self.id_permissao}, nome='{self.nome_permissao}')>"

class UsuarioPerfil(Base):
    __tablename__ = "usuario_perfil"

    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), primary_key=True)
    id_perfil = Column(Integer, ForeignKey("perfil.id_perfil"), primary_key=True)

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="perfis")
    perfil = relationship("Perfil", back_populates="usuarios")

    def __repr__(self):
        return f"<UsuarioPerfil(usuario_id={self.id_usuario}, perfil_id={self.id_perfil})>"

class PerfilPermissao(Base):
    __tablename__ = "perfil_permissao"

    id_perfil = Column(Integer, ForeignKey("perfil.id_perfil"), primary_key=True)
    id_permissao = Column(Integer, ForeignKey("permissao.id_permissao"), primary_key=True)

    # Relacionamentos
    perfil = relationship("Perfil", back_populates="permissoes")
    permissao = relationship("Permissao", back_populates="perfis")

    def __repr__(self):
        return f"<PerfilPermissao(perfil_id={self.id_perfil}, permissao_id={self.id_permissao})>"

class Atendimento(Base):
    __tablename__ = "atendimento"

    id_atendimento = Column(Integer, primary_key=True, index=True)
    data_atendimento = Column(DateTime, nullable=False)
    tipo_atendimento = Column(String(100), nullable=False)
    resumo = Column(Text, nullable=False)
    encaminhamentos = Column(Text)
    id_familia = Column(Integer, ForeignKey("familia.id_familia"), nullable=False)
    id_profissional = Column(Integer, ForeignKey("profissional.id_profissional"), nullable=False)
    id_pessoa_membro = Column(Integer, ForeignKey("pessoa.id_pessoa"))

    # Relacionamentos
    familia = relationship("Familia", back_populates="atendimentos")
    profissional = relationship("Profissional", back_populates="atendimentos")
    pessoa_membro = relationship("Pessoa", back_populates="atendimentos_membro")

    def __repr__(self):
        return f"<Atendimento(id={self.id_atendimento}, tipo='{self.tipo_atendimento}', data='{self.data_atendimento}')>"

class Beneficio(Base):
    __tablename__ = "beneficio"

    id_beneficio = Column(Integer, primary_key=True, index=True)
    tipo_beneficio = Column(String(100), nullable=False)
    valor_monetario = Column(Numeric(10, 2))
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date)
    observacoes = Column(Text)
    id_familia = Column(Integer, ForeignKey("familia.id_familia"), nullable=False)
    id_pessoa_membro = Column(Integer, ForeignKey("pessoa.id_pessoa"))

    # Relacionamentos
    familia = relationship("Familia", back_populates="beneficios")
    pessoa_membro = relationship("Pessoa", back_populates="beneficios_membro")

    def __repr__(self):
        return f"<Beneficio(id={self.id_beneficio}, tipo='{self.tipo_beneficio}')>"

class Necessidade(Base):
    __tablename__ = "necessidade"

    id_necessidade = Column(Integer, primary_key=True, index=True)
    tipo_necessidade = Column(String(100), nullable=False)
    descricao = Column(Text)
    grau_prioridade = Column(String(50), nullable=False)
    status_resolucao = Column(String(50), nullable=False)
    data_registro = Column(Date, default=datetime.now().date(), nullable=False)
    data_resolucao = Column(Date)
    id_familia = Column(Integer, ForeignKey("familia.id_familia"), nullable=False)

    # Relacionamento
    familia = relationship("Familia", back_populates="necessidades")

    def __repr__(self):
        return f"<Necessidade(id={self.id_necessidade}, tipo='{self.tipo_necessidade}', status='{self.status_resolucao}')>"

class Ocorrencia(Base):
    __tablename__ = "ocorrencia"

    id_ocorrencia = Column(Integer, primary_key=True, index=True)
    data_ocorrencia = Column(DateTime, nullable=False)
    tipo_ocorrencia = Column(String(100), nullable=False)
    descricao = Column(Text)
    id_profissional = Column(Integer, ForeignKey("profissional.id_profissional"))
    id_familia = Column(Integer, ForeignKey("familia.id_familia"), nullable=False)

    # Relacionamentos
    profissional = relationship("Profissional", back_populates="ocorrencias")
    familia = relationship("Familia", back_populates="ocorrencias")

    def __repr__(self):
        return f"<Ocorrencia(id={self.id_ocorrencia}, tipo='{self.tipo_ocorrencia}', data='{self.data_ocorrencia}')>"


def create_tables():
    Base.metadata.create_all(engine)

# Função para obter uma sessão de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

