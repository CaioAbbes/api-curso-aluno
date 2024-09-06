from flask import Flask, jsonify, request
from config import Config
from models import db, CursoAluno, Curso
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

   
@app.route('/get_curso_id', methods=['GET'])
def get_curso_id():
    try:
       
        id_aluno_entry = request.args.get('id_aluno')

        cursos_aluno = CursoAluno.query.filter_by(id_aluno = id_aluno_entry).all()

        cursos_json = []

        print(id_aluno_entry)
        print(cursos_aluno)

        for curso_aluno in cursos_aluno:
            curso = Curso.query.filter_by(id_curso = curso_aluno.id_curso).first()
            curso_data = {
                'id_curso': curso.id_curso,
                'titulo': curso.titulo,
                'sub_titulo': curso.sub_titulo,
                'descricao': curso.descricao,
                'preco': curso.preco,
                'imagem': curso.imagem,
                'id_professor': curso.id_professor
            }

            cursos_json.append(curso_data)

        if len(cursos_json) > 0:
            return jsonify({'Curso': True, 'Mensagem': cursos_json})
        
        return jsonify({'Curso': False, 'Mensagem': 'Aluno não matriculado em nenhum curso!'}), 404

    
    except Exception as e:
        logging.error(f"Erro no get_curso_id: {e}")
        db.session.rollback()
        return jsonify({'Curso': False, 'Mensagem': str(e)}), 500
    
@app.route('/aluno_matricula_curso', methods=['POST'])
def aluno_matricula_curso():
    try:
        id_curso_entry = request.args.get('id_curso')
        id_aluno_entry = request.args.get('id_aluno')

        curso_aluno = CursoAluno(id_curso = id_curso_entry, id_aluno = id_aluno_entry, status = 'Ativo')

        db.session.add(curso_aluno)
        db.session.commit()
        logging.info("Sucesso no aluno_matricula_curso")
        return jsonify({'Matriculado': True, 'Mensagem': {
            'id_aluno': curso_aluno.id_aluno,
            'id_curso': curso_aluno.id_curso,
            'data_matricula': curso_aluno.data_matricula,
            'data_conclusao': curso_aluno.data_conclusao,
            'status': curso_aluno.status,
            'nota_final': curso_aluno.nota_final,
            'comentarios': curso_aluno.comentarios
        }})
    
    except Exception as e:
        logging.error(f"Erro no aluno_matricula_curso {e}")
        return jsonify({'Matriculado': False, 'Mensagem': str(e)}), 500
    
@app.route('/delete_aluno_matricula_curso', methods=['POST'])
def delete_aluno_matricula_curso():
    try:
        id_aluno_entry = request.args.get('id_aluno')
        
        if not id_aluno_entry:
            return jsonify({'Erro': 'id nao digitado'}), 400
        
        curso_aluno = CursoAluno.query.filter_by(id_aluno=id_aluno_entry).first()
        
        if curso_aluno:
            db.session.delete(curso_aluno)
            db.session.commit()
            logging.info("Sucesso no delete_aluno_matricula_curso")
            return jsonify({'Deletado': True, 'Mensagem': 'Matricula deletada com sucesso"'})
        
        return jsonify({'Deletado': False, 'Mensagem': 'Aluno nao encontrado'}), 404
        
    except Exception as e:
        logging.error(f"Erro no delete_aluno_matricula_curso: {e}")
        db.session.rollback()
        return jsonify({'Deletado': False, 'Mensagem': str(e)}), 500
        
@app.route('/get_aluno_matricula_curso', methods=['GET'])
def get_aluno_matricula_curso():
    try:
        id_curso_entry = request.args.get('id_curso')
        id_aluno_entry = request.args.get('id_aluno')

        curso_aluno = CursoAluno.query.filter_by(id_curso = id_curso_entry, id_aluno = id_aluno_entry).first()

        if curso_aluno:
            return jsonify({'Matriculado': True, 'Mensagem': {
                'id_aluno': curso_aluno.id_aluno,
                'id_curso': curso_aluno.id_curso,
                'data_matricula': curso_aluno.data_matricula,
                'data_conclusao': curso_aluno.data_conclusao,
                'status': curso_aluno.status,
                'nota_final': curso_aluno.nota_final,
                'comentarios': curso_aluno.comentarios
            }})

        return jsonify({'Matriculado': False, 'Mensagem': 'Aluno não matriculado em nenhum curso!'}), 404
    
    except Exception as e:
        logging.error(f"Erro no get_aluno_matricula_curso {e}")
        return jsonify({'Matriculado': False, 'Mensagem': str(e)}), 500
  
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5004)
