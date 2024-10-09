import csv
import io
import mysql.connector
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, send_file, current_app
from db import get_db_connection  # 相对路径导入
from auth import role_required  # 导入权限控制装饰器
purchases_bp = Blueprint('purchases', __name__)


# 只允许 Admin 和 Warehouse 角色访问主表管理页面
@purchases_bp.route('/main_management')
@role_required(['Admin', 'Warehouse'])
def main_management():
    return render_template('main_management.html')


# 只允许 Admin 和 Warehouse 角色访问明细管理页面
@purchases_bp.route('/detail_management')
@role_required(['Admin', 'Warehouse'])
def detail_management():
    return render_template('detail_management.html')


@purchases_bp.route('/add_purchase_main', methods=['POST'])
@role_required(['Admin', 'Warehouse'])  # 限制添加采购主表的操作
def add_purchase_main():
    Eid = request.form['Eid']
    Pcount = int(request.form['Pcount'])
    Ptotal = float(request.form['Ptotal'])
    Pdate = request.form['Pdate']
    other = request.form['other']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if employee exists
    cursor.execute('SELECT * FROM tb_employee WHERE Eid=%s', (Eid,))
    employee = cursor.fetchone()
    if not employee:
        conn.close()
        return '员工编号不存在，请使用有效的编号'

    cursor.execute(
        'INSERT INTO tb_pay_main (Eid, Pcount, Ptotal, Pdate, other) VALUES (%s, %s, %s, %s, %s)',
        (Eid, Pcount, Ptotal, Pdate, other))
    conn.commit()
    conn.close()
    return redirect(url_for('purchases.main_management'))


@purchases_bp.route('/get_purchases_main', methods=['GET'])
def get_purchases_main():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_pay_main')
    purchases_main = cursor.fetchall()
    conn.close()

    purchases_main_list = [{
        'Pid': purchase[0],
        'Eid': purchase[1],
        'Pcount': purchase[2],
        'Ptotal': purchase[3],
        'Pdate': purchase[4],
        'other': purchase[5]
    } for purchase in purchases_main]

    return jsonify(purchases_main_list)



@purchases_bp.route('/get_purchase_main', methods=['GET'])
def get_purchase_main():
    Pid = request.args.get('Pid')
    if not Pid:
        return '缺少采购单号参数', 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_pay_main WHERE Pid=%s', (Pid,))
    purchase_main = cursor.fetchone()
    conn.close()

    if not purchase_main:
        return '采购主表不存在', 404

    purchase_main_dict = {
        'Pid': purchase_main[0],
        'Eid': purchase_main[1],
        'Pcount': purchase_main[2],
        'Ptotal': purchase_main[3],
        'Pdate': purchase_main[4],
        'other': purchase_main[5]
    }

    return jsonify(purchase_main_dict)



@purchases_bp.route('/update_purchase_main', methods=['POST'])
def update_purchase_main():
    Pid = int(request.form['Pid'])
    Eid = request.form['Eid']
    Pcount = int(request.form['Pcount'])
    Ptotal = float(request.form['Ptotal'])
    Pdate = request.form['Pdate']
    other = request.form['other']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if employee exists
    cursor.execute('SELECT * FROM tb_employee WHERE Eid=%s', (Eid,))
    employee = cursor.fetchone()
    if not employee:
        conn.close()
        return '员工编号不存在，请使用有效的编号'

    cursor.execute(
        'UPDATE tb_pay_main SET Eid=%s, Pcount=%s, Ptotal=%s, Pdate=%s, other=%s WHERE Pid=%s',
        (Eid, Pcount, Ptotal, Pdate, other, Pid))
    conn.commit()
    conn.close()
    return redirect(url_for('purchases.main_management'))


@purchases_bp.route('/delete_purchase_main', methods=['POST'])
def delete_purchase_main():
    Pid = int(request.form['Pid'])

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Delete related rows in tb_pay_detail
        cursor.execute('DELETE FROM tb_pay_detail WHERE Pid=%s', (Pid,))

        # Delete the purchase main record
        cursor.execute('DELETE FROM tb_pay_main WHERE Pid=%s', (Pid,))
        conn.commit()
        return '采购主表删除成功'
    except mysql.connector.Error as err:
        conn.rollback()
        current_app.logger.error(f'删除失败: {err}')
        return f'删除失败: {err}'
    finally:
        conn.close()



@purchases_bp.route('/add_purchase_detail', methods=['POST'])
def add_purchase_detail():
    Pid = int(request.form['Pid'])
    Gid = request.form['Gid']
    Pcount = int(request.form['Pcount'])
    GPay = float(request.form['GPay'])
    total = float(request.form['total'])
    other = request.form['other']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if purchase main exists
    cursor.execute('SELECT * FROM tb_pay_main WHERE Pid=%s', (Pid,))
    purchase_main = cursor.fetchone()
    if not purchase_main:
        conn.close()
        return '采购清单号不存在，请使用有效的编号'

    # Check if good exists
    cursor.execute('SELECT * FROM tb_good WHERE Gid=%s', (Gid,))
    good = cursor.fetchone()
    if not good:
        conn.close()
        return '商品编号不存在，请使用有效的编号'

    cursor.execute(
        'INSERT INTO tb_pay_detail (Pid, Gid, Pcount, GPay, total, other) VALUES (%s, %s, %s, %s, %s, %s)',
        (Pid, Gid, Pcount, GPay, total, other))
    conn.commit()
    conn.close()
    return redirect(url_for('purchases.detail_management'))


@purchases_bp.route('/get_purchases_detail', methods=['GET'])
def get_purchases_detail():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_pay_detail')
    purchases_detail = cursor.fetchall()
    conn.close()

    purchases_detail_list = [{
        'PDid': detail[0],
        'Pid': detail[1],
        'Gid': detail[2],
        'Pcount': detail[3],
        'GPay': detail[4],
        'total': detail[5],
        'other': detail[6]
    } for detail in purchases_detail]

    return jsonify(purchases_detail_list)



@purchases_bp.route('/get_purchase_detail', methods=['GET'])
def get_purchase_detail():
    PDid = int(request.args.get('PDid'))
    if not PDid:
        return '缺少采购明细号参数', 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_pay_detail WHERE PDid=%s', (PDid,))
    purchase_detail = cursor.fetchone()
    conn.close()

    if not purchase_detail:
        return '采购明细不存在', 404

    purchase_detail_dict = {
        'PDid': purchase_detail[0],
        'Pid': purchase_detail[1],
        'Gid': purchase_detail[2],
        'Pcount': purchase_detail[3],
        'GPay': purchase_detail[4],
        'total': purchase_detail[5],
        'other': purchase_detail[6]
    }

    return jsonify(purchase_detail_dict)



@purchases_bp.route('/update_purchase_detail', methods=['POST'])
def update_purchase_detail():
    PDid = int(request.form['PDid'])
    Pid = int(request.form['Pid'])
    Gid = request.form['Gid']
    Pcount = int(request.form['Pcount'])
    GPay = float(request.form['GPay'])
    total = float(request.form['total'])
    other = request.form['other']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if purchase main exists
    cursor.execute('SELECT * FROM tb_pay_main WHERE Pid=%s', (Pid,))
    purchase_main = cursor.fetchone()
    if not purchase_main:
        conn.close()
        return '采购清单号不存在，请使用有效的编号'

    # Check if good exists
    cursor.execute('SELECT * FROM tb_good WHERE Gid=%s', (Gid,))
    good = cursor.fetchone()
    if not good:
        conn.close()
        return '商品编号不存在，请使用有效的编号'

    cursor.execute(
        'UPDATE tb_pay_detail SET Pid=%s, Gid=%s, Pcount=%s, GPay=%s, total=%s, other=%s WHERE PDid=%s',
        (Pid, Gid, Pcount, GPay, total, other, PDid))
    conn.commit()
    conn.close()
    return redirect(url_for('purchases.detail_management'))


@purchases_bp.route('/delete_purchase_detail', methods=['POST'])
def delete_purchase_detail():
    PDid = int(request.form['PDid'])

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tb_pay_detail WHERE PDid=%s', (PDid,))
    conn.commit()
    conn.close()
    return '采购明细删除成功'


@purchases_bp.route('/export_purchases', methods=['GET'])
def export_purchases():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_pay_main')
    purchases_main = cursor.fetchall()

    cursor.execute('SELECT * FROM tb_pay_detail')
    purchases_detail = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Pid', 'Eid', 'Pcount', 'Ptotal', 'Pdate', 'other'])
    for row in purchases_main:
        writer.writerow(row)

    writer.writerow([])
    writer.writerow(['PDid', 'Pid', 'Gid', 'Pcount', 'GPay', 'total', 'other'])
    for row in purchases_detail:
        writer.writerow(row)

    output.seek(0)
    encoded_output = io.BytesIO(output.getvalue().encode('utf-8'))

    return send_file(encoded_output, mimetype='text/csv', download_name='purchases.csv', as_attachment=True)



@purchases_bp.route('/search_purchases_main', methods=['GET'])
def search_purchases_main():
    eid = request.args.get('eid', '').lower()
    pdate = request.args.get('pdate', '').lower()

    query = 'SELECT * FROM tb_pay_main WHERE LOWER(Eid) LIKE %s AND LOWER(Pdate) LIKE %s'
    params = (f'%{eid}%', f'%{pdate}%')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    purchases_main = cursor.fetchall()
    conn.close()

    purchases_main_list = [{
        'Pid': purchase[0],
        'Eid': purchase[1],
        'Pcount': purchase[2],
        'Ptotal': purchase[3],
        'Pdate': purchase[4],
        'other': purchase[5]
    } for purchase in purchases_main]

    return jsonify(purchases_main_list)


@purchases_bp.route('/search_purchases_detail', methods=['GET'])
def search_purchases_detail():
    pid = request.args.get('pid', '').lower()
    gid = request.args.get('gid', '').lower()

    query = 'SELECT * FROM tb_pay_detail WHERE LOWER(Pid) LIKE %s AND LOWER(Gid) LIKE %s'
    params = (f'%{pid}%', f'%{gid}%')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    purchases_detail = cursor.fetchall()
    conn.close()

    purchases_detail_list = [{
        'PDid': detail[0],
        'Pid': detail[1],
        'Gid': detail[2],
        'Pcount': detail[3],
        'GPay': detail[4],
        'total': detail[5],
        'other': detail[6]
    } for detail in purchases_detail]

    return jsonify(purchases_detail_list)
