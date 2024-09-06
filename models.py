from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Curso(db.Model):
    __tablename__ = 'curso'

    id_curso = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(300), nullable=False)
    sub_titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.String(300), nullable=False)
    preco = db.Column(db.Numeric(19, 2), nullable=False)
    imagem = db.Column(db.String(300), nullable=False)
    id_professor = db.Column(db.Integer, nullable=False)

class CursoAluno(db.Model):
    __tablename__ = 'curso_aluno'

    id_aluno = db.Column(db.Integer, db.ForeignKey('aluno.id_aluno'), primary_key=True)
    id_curso = db.Column(db.Integer, db.ForeignKey('curso.id_curso'), primary_key=True)
    data_matricula = db.Column(db.Date, default=datetime.datetime.now(), nullable=False)
    data_conclusao = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(30), nullable=False)
    nota_final = db.Column(db.Numeric(5, 2), nullable=True)
    comentarios = db.Column(db.String(300), nullable=True)

