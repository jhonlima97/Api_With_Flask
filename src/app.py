from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
conexion = MySQL(app)

@app.route('/v1/courses/', defaults={'id': None}, methods=['GET'])
@app.route('/v1/courses/<id>', methods=['GET'])
def list_courses(id):
    try:
        cursor = conexion.connection.cursor()
        if id is None:
            sql = "SELECT * FROM course"
        else:
            sql = "SELECT * FROM course WHERE code = '{0}' ".format(id)
        cursor.execute(sql)
        datos=cursor.fetchall()
        courses=[]
        for fila in datos:
            course={'code': fila[0], 'name': fila[1], 'credits': fila[2]}
            courses.append(course)
         # Si no se encontraron cursos, retorna "Codigo no existe"
        if not courses and id is not None:
            return jsonify({'message': "Codigo no existe"}), 404

        return jsonify({'courses':courses})
        #return jsonify({'courses':courses, 'message': "Listed Courses"})
    except Exception as ex:
        return jsonify({'message': "Error"})

@app.route('/v1/courses', methods=['POST'])
def add_course():
    try:
        # Obtén el ID del curso desde el request
        course_id = request.json['code']
        course_name = request.json['name']
        course_credits  = request.json['credits']

        # Verifica que el cod sea entero de 6
        if not str(course_id).isdigit() or len(str(course_id)) != 6:
            return jsonify({'message': "El codigo debe ser entero de longitud 6"}), 415

        # Verifica que el name sean solo letras y espacios
        if not all(x.isalpha() or x.isspace() for x in course_name):
            return jsonify({'message': "El name debe ser solo letras"}), 415
        # Verifica que el name no esté vacío
        if not course_name.strip():
            return jsonify({'message': "El name no puede estar vacío"}), 415

         
        # Verifica que los créditos sean numéricos y estén entre 1 y 9
        if not str(course_credits).isdigit() or int(course_credits) < 1 or int(course_credits) > 9:
            return jsonify({'message': "Los créditos deben ser un número entre 1 y 9"}), 415
        
        # Verifica que el cod sea único
        cursor = conexion.connection.cursor()
        cursor.execute("SELECT code FROM course WHERE code = %s", (course_id,))
        existing_id = cursor.fetchone()
        if existing_id is not None:
            return jsonify({'message': "El codigo ya existe"}), 406

        # Si el ID es válido, inserta el curso en la base de datos
        sql = """INSERT INTO course(code, name, credits) 
            VALUES ('{0}','{1}',{2})""".format(course_id, course_name, course_credits)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'message': "Course added successfully"})
    
    except Exception as ex:
        return jsonify({'message': "Error"})

@app.route('/v1/courses/<id>', methods=['PUT'])
def edit_course(id):
    try:
        # Obtén el name del curso desde el request
        course_name = request.json['name']
        course_credits  = request.json['credits']

        # Verifica que el name sean solo letras y espacios
        if not all(x.isalpha() or x.isspace() for x in course_name):
            return jsonify({'message': "El name debe ser solo letras"}), 415
        # Verifica que el name no esté vacío
        if not course_name.strip():
            return jsonify({'message': "El name no puede estar vacío"}), 415
        
        # Verifica que los créditos sean numéricos y estén entre 1 y 9
        if not str(course_credits).isdigit() or int(course_credits) < 1 or int(course_credits) > 9:
            return jsonify({'message': "Los créditos deben ser un número entre 1 y 9"}), 415
        
        # Verifica que el curso exista
        cursor = conexion.connection.cursor()
        cursor.execute("SELECT code FROM course WHERE code = %s", (id,))
        existing_id = cursor.fetchone()
        if existing_id is None:
            return jsonify({'message': "Codigo no existe"}), 404
            
        # Si el curso existe, actualiza el curso en la base de datos
        cursor = conexion.connection.cursor()
        sql = """UPDATE course SET name = '{0}', credits = {1} 
            WHERE code = '{2}'""".format(course_name, course_credits, id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'message': "Course updated successfully"})    
    except Exception as ex:
        return jsonify({'message': "Error"}), 500

@app.route('/v1/courses/<id>', methods=['DELETE'])
def delete_course(id):
    try:
        cursor = conexion.connection.cursor()
        # Verifica si el curso existe
        cursor.execute("SELECT code FROM course WHERE code = %s", (id,))
        existing_id = cursor.fetchone()

        # Si el curso no existe"
        if existing_id is None:
            return jsonify({'message': "Codigo no existe"}), 404

        # Si el curso existe, elimínalo
        sql = "DELETE FROM course WHERE code = '{0}'".format(id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'message': "Course deleted successfully"})

    except Exception as ex:
        return jsonify({'message': "Error"}), 500
    
def page_not_found(error):
    return "<h2> La página no existe</h2>"


if __name__ == '__main__':
    app.config.from_object(DevelopmentConfig)
    app.register_error_handler(404, page_not_found)
    app.run()