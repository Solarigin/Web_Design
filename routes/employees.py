import csv
import io
import mysql.connector
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, send_file, current_app
from db import get_db_connection  # 相对路径导入
from auth import role_required

employees_bp = Blueprint('employees', __name__)


@employees_bp.route('/employee_management')
@role_required(['Admin'])  # 仅允许管理员访问
def employee_management():
    return render_template('employee.html')


@employees_bp.route('/add_employee', methods=['POST'])
def add_employee():
    Eid = request.form['Eid']
    EName = request.form['EName']
    EPas = request.form['EPas']
    Elevel = request.form['Elevel']
    EtelPhone = request.form['EtelPhone']
    ESalary = request.form['ESalary']
    other = request.form['other']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if employee with the same Eid already exists
    cursor.execute('SELECT * FROM tb_employee WHERE Eid=%s', (Eid,))
    existing_employee = cursor.fetchone()
    if existing_employee:
        conn.close()
        return '员工编号已存在，请使用不同的编号'

    cursor.execute(
        'INSERT INTO tb_employee (Eid, EName, EPas, Elevel, EtelPhone, ESalary, other) VALUES (%s, %s, %s, %s, %s, %s, %s)',
        (Eid, EName, EPas, Elevel, EtelPhone, ESalary, other))
    conn.commit()
    conn.close()
    return redirect(url_for('employees.employee_management'))


@employees_bp.route('/get_employees', methods=['GET'])
def get_employees():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_employee')
    employees = cursor.fetchall()
    conn.close()

    employees_list = [{
        'Eid': employee[0],
        'EName': employee[1],
        'EPas': employee[2],
        'Elevel': employee[3],
        'EtelPhone': employee[4],
        'ESalary': employee[5],
        'other': employee[6]
    } for employee in employees]

    return jsonify(employees_list)


@employees_bp.route('/update_employee', methods=['POST'])
def update_employee():
    Eid = request.form['Eid']
    EName = request.form['EName']
    EPas = request.form['EPas']
    Elevel = request.form['Elevel']
    EtelPhone = request.form['EtelPhone']
    ESalary = request.form['ESalary']
    other = request.form['other']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE tb_employee SET EName=%s, EPas=%s, Elevel=%s, EtelPhone=%s, ESalary=%s, other=%s WHERE Eid=%s',
        (EName, EPas, Elevel, EtelPhone, ESalary, other, Eid))
    conn.commit()
    conn.close()
    return redirect(url_for('employees.employee_management'))


@employees_bp.route('/search_employees', methods=['GET'])
def search_employees():
    name = request.args.get('name', '').lower()
    phone = request.args.get('phone', '').lower()
    level = request.args.get('level', '').lower()

    query = 'SELECT * FROM tb_employee WHERE LOWER(EName) LIKE %s AND LOWER(EtelPhone) LIKE %s AND LOWER(Elevel) LIKE %s'
    params = (f'%{name}%', f'%{phone}%', f'%{level}%')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    employees = cursor.fetchall()
    conn.close()

    employees_list = [{
        'Eid': employee[0],
        'EName': employee[1],
        'EPas': employee[2],
        'Elevel': employee[3],
        'EtelPhone': employee[4],
        'ESalary': employee[5],
        'other': employee[6]
    } for employee in employees]

    return jsonify(employees_list)


@employees_bp.route('/delete_employee', methods=['POST'])
def delete_employee():
    Eid = request.form['Eid']

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if employee exists
        cursor.execute('SELECT * FROM tb_employee WHERE Eid=%s', (Eid,))
        employee = cursor.fetchone()
        if not employee:
            conn.close()
            return '员工不存在'

        # Delete related rows in tb_pay_detail and tb_pay_main will be handled by cascading delete
        cursor.execute('DELETE FROM tb_employee WHERE Eid=%s', (Eid,))

        conn.commit()
        return '员工删除成功'
    except mysql.connector.Error as err:
        conn.rollback()
        current_app.logger.error(f'删除失败: {err}')
        return f'删除失败: {err}'
    finally:
        conn.close()


@employees_bp.route('/get_employee', methods=['GET'])
def get_employee():
    Eid = request.args.get('Eid')
    if not Eid:
        return '缺少员工编号参数', 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_employee WHERE Eid=%s', (Eid,))
    employee = cursor.fetchone()
    conn.close()

    if not employee:
        return '员工不存在', 404

    return jsonify(employee)


@employees_bp.route('/export_employees', methods=['GET'])
def export_employees():
    name = request.args.get('name', '').lower()
    phone = request.args.get('phone', '').lower()
    level = request.args.get('level', '').lower()

    query = 'SELECT * FROM tb_employee WHERE LOWER(EName) LIKE %s AND LOWER(EtelPhone) LIKE %s AND LOWER(Elevel) LIKE %s'
    params = (f'%{name}%', f'%{phone}%', f'%{level}%')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    employees = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Eid', 'EName', 'EPas', 'Elevel', 'EtelPhone', 'ESalary', 'other'])
    for row in employees:
        writer.writerow(row)

    output.seek(0)
    encoded_output = io.BytesIO(output.getvalue().encode('utf-8'))

    return send_file(encoded_output, mimetype='text/csv', download_name='employees.csv', as_attachment=True)
