from sqlalchemy.orm import Session
from app.models.veiculo import Veiculo
from app.schemas.veiculo import VeiculoCreate, VeiculoUpdate


def criar(db: Session, veiculo: VeiculoCreate):
    db_veiculo = Veiculo(**veiculo.dict())
    db.add(db_veiculo)
    db.commit()
    db.refresh(db_veiculo)
    return db_veiculo


def listar(db: Session):
    return db.query(Veiculo).all()


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