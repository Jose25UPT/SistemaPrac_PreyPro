from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

db_config = {
    'host': os.getenv('DB_HOST', 'db'),
    'user': os.getenv('DB_USER', 'user_practicas'),
    'password': os.getenv('DB_PASSWORD', 'userpassword'),
    'db': os.getenv('DB_NAME', 'db_practicas'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**db_config)

# 📥 READ - Obtener todas las prácticas
@app.route('/api/practicas', methods=['GET'])
def get_practicas():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM practicas ORDER BY id DESC")
            data = cur.fetchall()
            # Convertir fechas a string para JSON
            for row in data:
                for key, value in row.items():
                    if isinstance(value, datetime):
                        row[key] = value.strftime('%Y-%m-%d')
            return jsonify(data)
    finally:
        conn.close()

# ➕ CREATE - Nueva práctica
@app.route('/api/practicas', methods=['POST'])
def create_practica():
    data = request.json
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            sql = """INSERT INTO practicas (
                cod_univ, raz_soc, facultad, prim_ape, seg_ape, nombre, sexo, tipo_doc, nro_doc,
                fecha_matri, fecha_egreso, ciclo_egreso, reg_oficio, codigo_practica, tipo_practica,
                empresa, area, cargo, abre_gyt, carrera, grado, programa, creditos, mod_obt, mod_est,
                fecha_inicio, resolucion, fecha_resol, dipl_fec_org, nro_diploma, reg_libro,
                reg_folio, reg_registro, cargo_1, autoridad_1, cargo_2, autoridad_2, cargo_3, autoridad_3
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            values = (
                data.get('cod_univ'), data.get('raz_soc'), data.get('facultad'), data.get('prim_ape'),
                data.get('seg_ape'), data.get('nombre'), data.get('sexo'), data.get('tipo_doc'), data.get('nro_doc'),
                data.get('fecha_matri'), data.get('fecha_egreso'), data.get('ciclo_egreso'), data.get('reg_oficio'),
                data.get('codigo_practica'), data.get('tipo_practica', 'PRE-PROFESIONAL'),  # ← NUEVO CAMPO
                data.get('empresa'), data.get('area'), data.get('cargo'), data.get('abre_gyt'),
                data.get('carrera'), data.get('grado'), data.get('programa'), data.get('creditos'),
                data.get('mod_obt'), data.get('mod_est'), data.get('fecha_inicio'), data.get('resolucion'),
                data.get('fecha_resol'), data.get('dipl_fec_org'), data.get('nro_diploma'),
                data.get('reg_libro'), data.get('reg_folio'), data.get('reg_registro'),
                data.get('cargo_1'), data.get('autoridad_1'), data.get('cargo_2'), data.get('autoridad_2'),
                data.get('cargo_3'), data.get('autoridad_3')
            )
            cur.execute(sql, values)
            conn.commit()
            return jsonify({'message': 'Práctica registrada con éxito', 'id': cur.lastrowid}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# ✏️ UPDATE - Editar práctica
@app.route('/api/practicas/<int:id>', methods=['PUT'])
def update_practica(id):
    data = request.json
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            sql = """UPDATE practicas SET
                cod_univ=%s, raz_soc=%s, facultad=%s, prim_ape=%s, seg_ape=%s, nombre=%s, 
                sexo=%s, tipo_doc=%s, nro_doc=%s, fecha_matri=%s, fecha_egreso=%s, ciclo_egreso=%s, 
                reg_oficio=%s, codigo_practica=%s, tipo_practica=%s, empresa=%s, area=%s, cargo=%s, 
                abre_gyt=%s, carrera=%s, grado=%s, programa=%s, creditos=%s, mod_obt=%s, mod_est=%s,
                fecha_inicio=%s, resolucion=%s, fecha_resol=%s, dipl_fec_org=%s, nro_diploma=%s, 
                reg_libro=%s, reg_folio=%s, reg_registro=%s, cargo_1=%s, autoridad_1=%s, 
                cargo_2=%s, autoridad_2=%s, cargo_3=%s, autoridad_3=%s
                WHERE id=%s"""
            
            values = (
                data.get('cod_univ'), data.get('raz_soc'), data.get('facultad'), data.get('prim_ape'),
                data.get('seg_ape'), data.get('nombre'), data.get('sexo'), data.get('tipo_doc'), data.get('nro_doc'),
                data.get('fecha_matri'), data.get('fecha_egreso'), data.get('ciclo_egreso'), data.get('reg_oficio'),
                data.get('codigo_practica'), data.get('tipo_practica', 'PRE-PROFESIONAL'),
                data.get('empresa'), data.get('area'), data.get('cargo'), data.get('abre_gyt'),
                data.get('carrera'), data.get('grado'), data.get('programa'), data.get('creditos'),
                data.get('mod_obt'), data.get('mod_est'), data.get('fecha_inicio'), data.get('resolucion'),
                data.get('fecha_resol'), data.get('dipl_fec_org'), data.get('nro_diploma'),
                data.get('reg_libro'), data.get('reg_folio'), data.get('reg_registro'),
                data.get('cargo_1'), data.get('autoridad_1'), data.get('cargo_2'), data.get('autoridad_2'),
                data.get('cargo_3'), data.get('autoridad_3'), id
            )
            cur.execute(sql, values)
            conn.commit()
            return jsonify({'message': 'Práctica actualizada con éxito'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# 🗑️ DELETE - Eliminar práctica
@app.route('/api/practicas/<int:id>', methods=['DELETE'])
def delete_practica(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM practicas WHERE id = %s", (id,))
            conn.commit()
            return jsonify({'message': 'Eliminado correctamente'}), 200
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)