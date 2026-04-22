from sqlalchemy.orm import Session
from app.models.veiculo import Veiculo
from app.schemas.veiculo import VeiculoCreate, VeiculoUpdate

from sqlalchemy import or_, cast, String
from typing import Optional


def criar(db: Session, veiculo: VeiculoCreate):
    db_veiculo = Veiculo(**veiculo.dict())
    db.add(db_veiculo)
    db.commit()
    db.refresh(db_veiculo)
    return db_veiculo



def listar(
    db: Session,
    search: Optional[str] = None,
    placa: Optional[str] = None,
    modelo: Optional[str] = None,
    marca: Optional[str] = None,
    ano: Optional[str] = None,
    VIN: Optional[str] = None,
    tipo: Optional[str] = None
):
    query = db.query(Veiculo)

    # Pesquisa geral
    if search:
        query = query.filter(
            or_(
                Veiculo.placa.contains(search),
                Veiculo.modelo.contains(search),
                Veiculo.marca.contains(search),
                cast(Veiculo.ano, String).contains(search),
                Veiculo.VIN.contains(search),
                Veiculo.tipo.contains(search)
            )
        )

    # Filtros específicos
    if placa:
        query = query.filter(Veiculo.placa.contains(placa))

    if modelo:
        query = query.filter(Veiculo.modelo.contains(modelo))

    if marca:
        query = query.filter(Veiculo.marca.contains(marca))

    if ano:
        query = query.filter(
            cast(Veiculo.ano, String).contains(ano)
        )

    if VIN:
        query = query.filter(Veiculo.VIN.contains(VIN))

    if tipo:
        query = query.filter(Veiculo.tipo.contains(tipo))

    return query.all()



def obter(db: Session, id: str):
    return db.query(Veiculo).filter(Veiculo.id == id).first()

def atualizar(db: Session, id: str, dados):
    veiculo = db.query(Veiculo).filter(Veiculo.id == id).first()

    if not veiculo:
        return None

    # verificar placa duplicada
    placa_existe = db.query(Veiculo).filter(
        Veiculo.placa == dados.placa,
        Veiculo.id != id
    ).first()

    if placa_existe:
        raise Exception("Já existe um veículo com essa placa")

    for key, value in dados.dict().items():
        setattr(veiculo, key, value)

    db.commit()
    db.refresh(veiculo)

    return veiculo



def deletar(db: Session, id: str):
    veiculo = obter(db, id)
    db.delete(veiculo)
    db.commit()