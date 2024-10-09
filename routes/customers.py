import csv
import io
import mysql.connector
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, send_file, current_app
from db import get_db_connection  # 相对路径导入
from auth import role_required  # 导入装饰器

customers_bp = Blueprint('customers', __name__)


# 只有 Admin 和 CustomerManager 可以访问此视图
@customers_bp.route('/customer_management')
@role_required(['Admin', 'CustomerManager'])
def customer_management():
    return render_template('customer.html')


@customers_bp.route('/add_customer', methods=['POST'])
def add_customer():
    CcompanyName = request.form['CcompanyName']
    CcompanySName = request.form['CcompanySName']
    CcompanyAddress = request.form['CcompanyAddress']
    CcompanyPhone = request.form['CcompanyPhone']
    Cemail = request.form['Cemail']
    Cname = request.form['Cname']
    CtelPhone = request.form['CtelPhone']
    other = request.form['other']

    conn = get_db_connection()
    cursor = conn.cursor()

    # 获取当前最大客户编号
    cursor.execute('SELECT Cid FROM tb_customer ORDER BY Cid DESC LIMIT 1')
    result = cursor.fetchone()
    if result:
        max_cid = result[0]
        next_cid_num = int(max_cid[1:]) + 1
        Cid = f'C{next_cid_num:03d}'  # 确保编号格式为CXXX
    else:
        Cid = 'C001'  # 如果没有记录，从C001开始

    cursor.execute(
        'INSERT INTO tb_customer (Cid, CcompanyName, CcompanySName, CcompanyAddress, CcompanyPhone, Cemail, Cname, CtelPhone, other) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (Cid, CcompanyName, CcompanySName, CcompanyAddress, CcompanyPhone, Cemail, Cname, CtelPhone, other))
    conn.commit()
    conn.close()
    return redirect(url_for('customers.customer_management'))


@customers_bp.route('/get_customers', methods=['GET'])
def get_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.callproc('GetAllCustomers')

    customers = []
    for result in cursor.stored_results():
        customers = result.fetchall()

    conn.close()

    customers_list = [{
        'Cid': customer[0],
        'CcompanyName': customer[1],
        'CcompanySName': customer[2],
        'CcompanyAddress': customer[3],
        'CcompanyPhone': customer[4],
        'Cemail': customer[5],
        'Cname': customer[6],
        'CtelPhone': customer[7],
        'other': customer[8]
    } for customer in customers]

    return jsonify(customers_list)


# 修改客户信息
@customers_bp.route('/update_customer', methods=['POST'])
def update_customer():
    Cid = request.form['Cid']
    CcompanyName = request.form['CcompanyName']
    CcompanySName = request.form['CcompanySName']
    CcompanyAddress = request.form['CcompanyAddress']
    CcompanyPhone = request.form['CcompanyPhone']
    Cemail = request.form['Cemail']
    Cname = request.form['Cname']
    CtelPhone = request.form['CtelPhone']
    other = request.form['other']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE tb_customer SET CcompanyName=%s, CcompanySName=%s, CcompanyAddress=%s, CcompanyPhone=%s, Cemail=%s, Cname=%s, CtelPhone=%s, other=%s WHERE Cid=%s',
        (CcompanyName, CcompanySName, CcompanyAddress, CcompanyPhone, Cemail, Cname, CtelPhone, other, Cid))
    conn.commit()
    conn.close()
    return redirect(url_for('customers.customer_management'))  # 更改这里的端点名称


@customers_bp.route('/search_customers', methods=['GET'])
def search_customers():
    name = request.args.get('name', '').lower()
    address = request.args.get('address', '').lower()
    contact = request.args.get('contact', '').lower()

    query = 'SELECT * FROM tb_customer WHERE LOWER(CcompanyName) LIKE %s AND LOWER(CcompanyAddress) LIKE %s AND LOWER(Cname) LIKE %s'
    params = (f'%{name}%', f'%{address}%', f'%{contact}%')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    customers = cursor.fetchall()
    conn.close()

    customers_list = [{
        'Cid': customer[0],
        'CcompanyName': customer[1],
        'CcompanySName': customer[2],
        'CcompanyAddress': customer[3],
        'CcompanyPhone': customer[4],
        'Cemail': customer[5],
        'Cname': customer[6],
        'CtelPhone': customer[7],
        'other': customer[8]
    } for customer in customers]

    return jsonify(customers_list)


# 删除客户信息 触发器删除
@customers_bp.route('/delete_customer', methods=['POST'])
def delete_customer():
    Cid = request.form['Cid']

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if the customer exists
        cursor.execute('SELECT * FROM tb_customer WHERE Cid=%s', (Cid,))
        customer = cursor.fetchone()
        if not customer:
            return '客户不存在'

        # Delete the customer, cascading delete will be handled by the database
        cursor.execute('DELETE FROM tb_customer WHERE Cid=%s', (Cid,))

        conn.commit()
        return '客户删除成功'
    except mysql.connector.Error as err:
        conn.rollback()
        current_app.logger.error(f'删除失败: {err}')
        return f'删除失败: {err}'
    finally:
        conn.close()


# 获取单个客户信息
@customers_bp.route('/get_customer', methods=['GET'])
def get_customer():
    Cid = request.args.get('Cid')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_customer WHERE Cid=%s', (Cid,))
    customer = cursor.fetchone()
    conn.close()
    return jsonify(customer)


# OutPutCSV
@customers_bp.route('/export_customers', methods=['GET'])
def export_customers():
    name = request.args.get('name', '').lower()
    address = request.args.get('address', '').lower()
    contact = request.args.get('contact', '').lower()

    query = 'SELECT * FROM tb_customer WHERE LOWER(CcompanyName) LIKE %s AND LOWER(CcompanyAddress) LIKE %s AND LOWER(Cname) LIKE %s'
    params = (f'%{name}%', f'%{address}%', f'%{contact}%')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    customers = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output, dialect='excel')
    writer.writerow(
        ['Cid', 'CcompanyName', 'CcompanySName', 'CcompanyAddress', 'CcompanyPhone', 'Cemail', 'Cname', 'CtelPhone',
         'other'])
    for row in customers:
        writer.writerow(row)

    output.seek(0)
    encoded_output = io.BytesIO(output.getvalue().encode('utf-8'))

    return send_file(encoded_output, mimetype='text/csv', download_name='customers.csv', as_attachment=True)
