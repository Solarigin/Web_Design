import csv
import io
import mysql.connector
from flask import Blueprint, request, jsonify, render_template, send_file, current_app
from db import get_db_connection  # 相对路径导入
from auth import role_required

goods_bp = Blueprint('goods', __name__)


@goods_bp.route('/good_management')
@role_required(['Admin', 'Warehouse'])  # 仅允许管理员和仓库管理角色访问
def good_management():
    return render_template('good.html')


@goods_bp.route('/get_good_price', methods=['GET'])
def get_good_price():
    Gid = request.args.get('Gid')
    if not Gid:
        return jsonify({'error': '缺少商品编号参数'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT GPay FROM tb_good WHERE Gid=%s', (Gid,))
    good = cursor.fetchone()
    conn.close()

    if not good:
        return jsonify({'error': '商品不存在'}), 404

    return jsonify({'GPay': good[0]})


@goods_bp.route('/add_good', methods=['POST'])
def add_good():
    # 自动生成 Gid
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT Gid FROM tb_good ORDER BY Gid DESC LIMIT 1')
    result = cursor.fetchone()

    if result:
        max_gid = result[0]
        next_gid_num = int(max_gid[1:]) + 1
        Gid = f'G{next_gid_num:03d}'  # 确保编号格式为GXXX
    else:
        Gid = 'G001'  # 如果没有记录，从G001开始

    Gname = request.form['GName']
    GPay = request.form['GPay']
    Cid = request.form['Cid']
    Gintroduction = request.form['GIntroduction']
    other = request.form['other']

    # 检查供应商是否存在
    cursor.execute('SELECT * FROM tb_customer WHERE Cid=%s', (Cid,))
    supplier = cursor.fetchone()
    if not supplier:
        conn.close()
        return '供应商编号不存在，请使用有效的编号'

    try:
        cursor.execute(
            'INSERT INTO tb_good (Gid, GName, GPay, Cid, GIntroduction, other) VALUES (%s, %s, %s, %s, %s, %s)',
            (Gid, Gname, GPay, Cid, Gintroduction, other))
        conn.commit()
        return '商品添加成功'
    except mysql.connector.Error as err:
        conn.rollback()
        current_app.logger.error(f'添加失败: {err}')
        return f'添加失败: {err}'
    finally:
        conn.close()


@goods_bp.route('/get_goods', methods=['GET'])
def get_goods():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_good')
    goods = cursor.fetchall()
    conn.close()

    goods_list = [{
        'Gid': good[0],
        'GName': good[1],
        'GPay': good[2],
        'Cid': good[3],
        'GIntroduction': good[4],
        'other': good[5]
    } for good in goods]

    return jsonify(goods_list)


@goods_bp.route('/get_good', methods=['GET'])
def get_good():
    Gid = request.args.get('Gid')
    if not Gid:
        return '缺少商品编号参数', 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_good WHERE Gid=%s', (Gid,))
    good = cursor.fetchone()
    conn.close()

    if not good:
        return '商品不存在', 404

    good_dict = {
        'Gid': good[0],
        'GName': good[1],
        'GPay': good[2],
        'Cid': good[3],
        'GIntroduction': good[4],
        'other': good[5]
    }

    return jsonify(good_dict)


# 新增一个用于获取下一个商品编号的路由
@goods_bp.route('/get_next_good_id', methods=['GET'])
def get_next_good_id():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT Gid FROM tb_good ORDER BY Gid DESC LIMIT 1')
    result = cursor.fetchone()

    if result:
        max_gid = result[0]
        next_gid_num = int(max_gid[1:]) + 1
        next_gid = f'G{next_gid_num:03d}'  # 确保编号格式为GXXX
    else:
        next_gid = 'G001'  # 如果没有记录，从G001开始

    conn.close()
    return jsonify({'nextGid': next_gid})


@goods_bp.route('/update_good', methods=['POST'])
def update_good():
    Gid = request.form['Gid']
    Gname = request.form['GName']
    GPay = request.form['GPay']
    Cid = request.form['Cid']
    Gintroduction = request.form['GIntroduction']
    other = request.form['other']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if supplier exists
    cursor.execute('SELECT * FROM tb_customer WHERE Cid=%s', (Cid,))
    supplier = cursor.fetchone()
    if not supplier:
        conn.close()
        return '供应商编号不存在，请使用有效的编号'

    try:
        cursor.execute(
            'UPDATE tb_good SET GName=%s, GPay=%s, Cid=%s, GIntroduction=%s, other=%s WHERE Gid=%s',
            (Gname, GPay, Cid, Gintroduction, other, Gid))
        conn.commit()
        return '商品更新成功'
    except mysql.connector.Error as err:
        conn.rollback()
        current_app.logger.error(f'更新失败: {err}')
        return f'更新失败: {err}'
    finally:
        conn.close()


@goods_bp.route('/search_goods', methods=['GET'])
def search_goods():
    name = request.args.get('name', '').lower()
    price = request.args.get('price', '').lower()
    supplier_id = request.args.get('supplier_id', '').lower()

    query = 'SELECT * FROM tb_good WHERE LOWER(GName) LIKE %s AND LOWER(CAST(GPay AS CHAR)) LIKE %s AND LOWER(Cid) LIKE %s'
    params = (f'%{name}%', f'%{price}%', f'%{supplier_id}%')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    goods = cursor.fetchall()
    conn.close()

    goods_list = [{
        'Gid': good[0],
        'GName': good[1],
        'GPay': good[2],
        'Cid': good[3],
        'GIntroduction': good[4],
        'other': good[5]
    } for good in goods]

    return jsonify(goods_list)


@goods_bp.route('/delete_good', methods=['POST'])
def delete_good():
    Gid = request.form['Gid']

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM tb_good WHERE Gid=%s', (Gid,))
        conn.commit()
        return '商品删除成功'
    except mysql.connector.Error as err:
        conn.rollback()
        current_app.logger.error(f'删除失败: {err}')
        return f'删除失败: {err}'
    finally:
        conn.close()


@goods_bp.route('/export_goods', methods=['GET'])
def export_goods():
    name = request.args.get('name', '').lower()
    price = request.args.get('price', '').lower()
    supplier_id = request.args.get('supplier_id', '').lower()

    query = 'SELECT * FROM tb_good WHERE LOWER(GName) LIKE %s AND LOWER(CAST(GPay AS CHAR)) LIKE %s AND LOWER(Cid) LIKE %s'
    params = (f'%{name}%', f'%{price}%', f'%{supplier_id}%')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    goods = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Gid', 'GName', 'GPay', 'Cid', 'GIntroduction', 'other'])
    for row in goods:
        writer.writerow(row)

    output.seek(0)
    encoded_output = io.BytesIO(output.getvalue().encode('utf-8'))

    return send_file(encoded_output, mimetype='text/csv', download_name='goods.csv', as_attachment=True)
