from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date, datetime
from typing import List, Optional
from decimal import Decimal 

from python.database import Pessoa, Familia, MembroDaFamilia, Profissional, Usuario, Perfil, Permissao, \
                     UsuarioPerfil, PerfilPermissao, Atendimento, Beneficio, Necessidade, Ocorrencia, \
                     engine, SessionLocal



def get_pessoa(db: Session, pessoa_id: int) -> Optional[Pessoa]:
    """Retorna uma pessoa pelo ID."""
    return db.query(Pessoa).filter(Pessoa.id_pessoa == pessoa_id).first()

def get_pessoas(db: Session, skip: int = 0, limit: int = 100) -> List[Pessoa]:
    """Retorna uma lista de pessoas."""
    return db.query(Pessoa).offset(skip).limit(limit).all()

def create_pessoa(db: Session, nome_completo: str, data_nasc: Optional[date], cpf: str,
                   rg: Optional[str], genero: Optional[str], email: str, telefone: Optional[str]) -> Pessoa:
    """Cria uma nova pessoa no banco de dados."""
    db_pessoa = Pessoa(
        nome_completo=nome_completo,
        data_nasc=data_nasc,
        cpf=cpf,
        rg=rg,
        genero=genero,
        email=email,
        telefone=telefone
    )
    db.add(db_pessoa)
    db.commit()    
    db.refresh(db_pessoa)
    return db_pessoa

def update_pessoa(db: Session, pessoa_id: int, nome_completo: Optional[str] = None,
                   data_nasc: Optional[date] = None, cpf: Optional[str] = None,
                   rg: Optional[str] = None, genero: Optional[str] = None,
                   email: Optional[str] = None, telefone: Optional[str] = None) -> Optional[Pessoa]:
    """Atualiza os dados de uma pessoa existente."""
    db_pessoa = get_pessoa(db, pessoa_id)
    if db_pessoa:
        if nome_completo is not None:
            db_pessoa.nome_completo = nome_completo
        if data_nasc is not None:
            db_pessoa.data_nasc = data_nasc
        if cpf is not None:
            db_pessoa.cpf = cpf
        if rg is not None:
            db_pessoa.rg = rg
        if genero is not None:
            db_pessoa.genero = genero
        if email is not None:
            db_pessoa.email = email
        if telefone is not None:
            db_pessoa.telefone = telefone
        db.commit()
        db.refresh(db_pessoa)
    return db_pessoa

def delete_pessoa(db: Session, pessoa_id: int) -> bool:
    """Deleta uma pessoa pelo ID."""
    db_pessoa = get_pessoa(db, pessoa_id)
    if db_pessoa:
        db.delete(db_pessoa)
        db.commit()
        return True
    return False

# --- Funções CRUD para Familia ---

def get_familia(db: Session, familia_id: int) -> Optional[Familia]:
    """Retorna uma família pelo ID."""
    return db.query(Familia).filter(Familia.id_familia == familia_id).first()

def get_familias(db: Session, skip: int = 0, limit: int = 100) -> List[Familia]:
    """Retorna uma lista de famílias."""
    return db.query(Familia).offset(skip).limit(limit).all()

def create_familia(db: Session, nome_familia: str, endereco: str, bairro: Optional[str],
                    cidade: Optional[str], estado: Optional[str], cep: str, telefone: str,
                    renda_mensal: Optional[float], status_vulnerabilidade: bool, observacoes: Optional[str]) -> Familia:
    """Cria uma nova família no banco de dados."""
    db_familia = Familia(
        nome_familia=nome_familia,
        endereco=endereco,
        bairro=bairro,
        cidade=cidade,
        estado=estado,
        cep=cep,
        telefone=telefone,
        renda_mensal=renda_mensal,
        data_cadastro=date.today(), 
        status_vulnerabilidade=status_vulnerabilidade,
        observacoes=observacoes
    )
    db.add(db_familia)
    db.commit()
    db.refresh(db_familia)
    return db_familia

def update_familia(db: Session, familia_id: int, nome_familia: Optional[str] = None, endereco: Optional[str] = None,
                   bairro: Optional[str] = None, cidade: Optional[str] = None, estado: Optional[str] = None,
                   cep: Optional[str] = None, telefone: Optional[str] = None, renda_mensal: Optional[float] = None,
                   status_vulnerabilidade: Optional[bool] = None, observacoes: Optional[str] = None) -> Optional[Familia]:
    """Atualiza os dados de uma família existente."""
    db_familia = get_familia(db, familia_id)
    if db_familia:
        if nome_familia is not None:
            db_familia.nome_familia = nome_familia
        if endereco is not None:
            db_familia.endereco = endereco
        if bairro is not None:
            db_familia.bairro = bairro
        if cidade is not None:
            db_familia.cidade = cidade
        if estado is not None:
            db_familia.estado = estado
        if cep is not None:
            db_familia.cep = cep
        if telefone is not None:
            db_familia.telefone = telefone
        if renda_mensal is not None:
            db_familia.renda_mensal = renda_mensal
        if status_vulnerabilidade is not None:
            db_familia.status_vulnerabilidade = status_vulnerabilidade
        if observacoes is not None:
            db_familia.observacoes = observacoes
        db.commit()
        db.refresh(db_familia)
    return db_familia

def delete_familia(db: Session, familia_id: int) -> bool:
    """Deleta uma família pelo ID."""
    db_familia = get_familia(db, familia_id)
    if db_familia:
        db.delete(db_familia)
        db.commit()
        return True
    return False

def execute_raw_query(query_string: str) -> List[dict]:
    """
    Executa uma query SQL bruta e retorna os resultados como uma lista de dicionários.
    Útil para operações que não se encaixam facilmente no ORM ou para depuração.
    """
    with engine.connect() as connection:
        result = connection.execute(text(query_string))
        # Para SELECTs, fetch os resultados
        if result.returns_rows: # <--- O 'if' ao qual o 'else' deve estar alinhado
            column_names = result.keys()
            # Converte cada linha em um dicionário e trata Decimal para float
            processed_rows = []
            for row in result.fetchall():
                # Cria um dicionário para a linha
                row_dict = dict(zip(column_names, row))
                # Itera sobre os valores do dicionário para converter Decimal
                for key, value in row_dict.items():
                    if isinstance(value, Decimal):
                        row_dict[key] = float(value)
                processed_rows.append(row_dict)
            return processed_rows # Retorna a lista de dicionários processados
        else: # <--- ESTE 'else' precisa estar alinhado com o 'if' acima
            # Para INSERT/UPDATE/DELETE, retorna uma lista vazia ou um status
            return []