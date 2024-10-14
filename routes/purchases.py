import csv
import io
import datetime
from flask import (
    Blueprint, request, jsonify, render_template, redirect,
    url_for, send_file, current_app, abort
)
from db import get_db_connection
from auth import role_required

purchases_bp = Blueprint('purchases', __name__)


# 主表管理页面，管理员和仓库角色可访问
@purchases_bp.route('/main_management')
@role_required(['Admin', 'Warehouse'])
def main_management():
    return render_template('main_management.html')


# 明细管理页面，管理员和仓库角色可访问
@purchases_bp.route('/detail_management')
@role_required(['Admin', 'Warehouse'])
def detail_management():
    return render_template('detail_management.html')


@purchases_bp.route('/add_purchase_main', methods=['POST'])
@role_required(['Admin', 'Warehouse'])
def add_purchase_main():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '未提供输入数据'}), 400

        Eid = data.get('Eid')
        Pdate = data.get('Pdate', datetime.date.today().strftime('%Y-%m-%d'))
        other = data.get('other', '')
        Pcount = 0  # 初始值
        Ptotal = 0.0  # 初始值

        if not Eid:
            return jsonify({'error': '缺少必填字段 Eid'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # 检查员工是否存在
        cursor.execute('SELECT * FROM tb_employee WHERE Eid=%s', (Eid,))
        employee = cursor.fetchone()
        if not employee:
            return jsonify({'error': '员工编号不存在'}), 400

        # 插入新记录，让数据库自动生成主键
        cursor.execute(
            'INSERT INTO tb_pay_main (Eid, Pcount, Ptotal, Pdate, other) '
            'VALUES (%s, %s, %s, %s, %s)',
            (Eid, Pcount, Ptotal, Pdate, other)
        )
        conn.commit()

        # 获取新插入记录的 Pid
        new_pid = cursor.lastrowid

        return jsonify({'message': '成功添加采购主表记录', 'Pid': new_pid}), 201
    except Exception as e:
        current_app.logger.error(f'添加采购主表时出错: {e}')
        return jsonify({'error': '添加采购主表记录失败'}), 500
    finally:
        cursor.close()
        conn.close()


@purchases_bp.route('/get_purchases_main', methods=['GET'])
@role_required(['Admin', 'Warehouse'])
def get_purchases_main():
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 50))
        offset = (page - 1) * page_size

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM tb_pay_main ORDER BY Pid LIMIT %s OFFSET %s',
            (page_size, offset)
        )
        purchases_main = cursor.fetchall()

        purchases_main_list = [{
            'Pid': purchase[0],
            'Eid': purchase[1],
            'Pcount': purchase[2],
            'Ptotal': purchase[3],
            'Pdate': purchase[4],
            'other': purchase[5]
        } for purchase in purchases_main]

        return jsonify(purchases_main_list)
    except Exception as e:
        current_app.logger.error(f'获取采购主表时出错: {e}')
        return jsonify({'error': '获取采购主表记录失败'}), 500
    finally:
        cursor.close()
        conn.close()


@purchases_bp.route('/get_purchase_main', methods=['GET'])
@role_required(['Admin', 'Warehouse'])
def get_purchase_main():
    try:
        Pid = request.args.get('Pid')
        if not Pid:
            return jsonify({'error': '缺少 Pid 参数'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tb_pay_main WHERE Pid=%s', (Pid,))
        purchase_main = cursor.fetchone()

        if not purchase_main:
            return jsonify({'error': '未找到采购主表记录'}), 404

        purchase_main_dict = {
            'Pid': purchase_main[0],
            'Eid': purchase_main[1],
            'Pcount': purchase_main[2],
            'Ptotal': purchase_main[3],
            'Pdate': purchase_main[4],
            'other': purchase_main[5]
        }

        return jsonify(purchase_main_dict)
    except Exception as e:
        current_app.logger.error(f'获取采购主表详情时出错: {e}')
        return jsonify({'error': '获取采购主表详情失败'}), 500
    finally:
        cursor.close()
        conn.close()


@purchases_bp.route('/update_purchase_main', methods=['POST'])
@role_required(['Admin', 'Warehouse'])
def update_purchase_main():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '未提供输入数据'}), 400

        Pid = data.get('Pid')
        Eid = data.get('Eid')
        Pdate = data.get('Pdate')
        other = data.get('other', '')

        if not Pid or not Eid or not Pdate:
            return jsonify({'error': '缺少必填字段'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # 检查员工是否存在
        cursor.execute('SELECT * FROM tb_employee WHERE Eid=%s', (Eid,))
        employee = cursor.fetchone()
        if not employee:
            return jsonify({'error': '员工编号不存在'}), 400

        # 更新可编辑字段
        cursor.execute(
            'UPDATE tb_pay_main SET Eid=%s, Pdate=%s, other=%s WHERE Pid=%s',
            (Eid, Pdate, other, Pid)
        )
        conn.commit()

        return jsonify({'message': '成功更新采购主表记录'}), 200
    except Exception as e:
        current_app.logger.error(f'更新采购主表时出错: {e}')
        return jsonify({'error': '更新采购主表记录失败'}), 500
    finally:
        cursor.close()
        conn.close()


@purchases_bp.route('/delete_purchase_main', methods=['POST'])
@role_required(['Admin', 'Warehouse'])
def delete_purchase_main():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '未提供输入数据'}), 400

        Pid = data.get('Pid')

        if not Pid:
            return jsonify({'error': '缺少 Pid 参数'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # 删除采购主表记录，并级联删除相关明细
        cursor.execute('DELETE FROM tb_pay_main WHERE Pid=%s', (Pid,))
        conn.commit()

        return jsonify({'message': '成功删除采购主表记录'}), 200
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f'删除采购主表时出错: {e}')
        return jsonify({'error': '删除采购主表记录失败'}), 500
    finally:
        cursor.close()
        conn.close()


@purchases_bp.route('/add_purchase_detail', methods=['POST'])
@role_required(['Admin', 'Warehouse'])
def add_purchase_detail():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '未提供输入数据'}), 400

        Pid = data.get('Pid')
        Gid = data.get('Gid')
        Pcount = data.get('Pcount')
        other = data.get('other', '')

        if not Pid or not Gid or not Pcount:
            return jsonify({'error': '缺少必填字段'}), 400

        try:
            Pcount = int(Pcount)
        except ValueError:
            return jsonify({'error': 'Pcount 必须是整数'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # 检查采购主表是否存在
        cursor.execute('SELECT * FROM tb_pay_main WHERE Pid=%s', (Pid,))
        purchase_main = cursor.fetchone()
        if not purchase_main:
            return jsonify({'error': '采购主表记录不存在'}), 400

        # 检查商品是否存在并获取 GPay
        cursor.execute('SELECT GPay FROM tb_good WHERE Gid=%s', (Gid,))
        good = cursor.fetchone()
        if not good:
            return jsonify({'error': '商品编号不存在'}), 400
        GPay = good[0]

        total = Pcount * GPay

        # 插入新的明细记录，让数据库自动生成 PDid
        cursor.execute(
            'INSERT INTO tb_pay_detail (Pid, Gid, Pcount, GPay, total, other) '
            'VALUES (%s, %s, %s, %s, %s, %s)',
            (Pid, Gid, Pcount, GPay, total, other)
        )

        # 更新采购主表的 Pcount 和 Ptotal
        cursor.execute('SELECT SUM(Pcount), SUM(total) FROM tb_pay_detail WHERE Pid=%s', (Pid,))
        sum_pcount, sum_total = cursor.fetchone()
        cursor.execute('UPDATE tb_pay_main SET Pcount=%s, Ptotal=%s WHERE Pid=%s', (sum_pcount, sum_total, Pid))

        conn.commit()

        # 获取新插入记录的 PDid
        new_pdid = cursor.lastrowid

        return jsonify({'message': '成功添加采购明细记录', 'PDid': new_pdid}), 201
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f'添加采购明细时出错: {e}')
        return jsonify({'error': '添加采购明细记录失败'}), 500
    finally:
        cursor.close()
        conn.close()


@purchases_bp.route('/get_purchases_detail', methods=['GET'])
@role_required(['Admin', 'Warehouse'])
def get_purchases_detail():
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 50))
        offset = (page - 1) * page_size

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM tb_pay_detail ORDER BY PDid LIMIT %s OFFSET %s',
            (page_size, offset)
        )
        purchases_detail = cursor.fetchall()

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
    except Exception as e:
        current_app.logger.error(f'获取采购明细时出错: {e}')
        return jsonify({'error': '获取采购明细记录失败'}), 500
    finally:
        cursor.close()
        conn.close()


@purchases_bp.route('/get_purchase_detail', methods=['GET'])
@role_required(['Admin', 'Warehouse'])
def get_purchase_detail():
    try:
        PDid = request.args.get('PDid')
        if not PDid:
            return jsonify({'error': '缺少 PDid 参数'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tb_pay_detail WHERE PDid=%s', (PDid,))
        purchase_detail = cursor.fetchone()

        if not purchase_detail:
            return jsonify({'error': '未找到采购明细记录'}), 404

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
    except Exception as e:
        current_app.logger.error(f'获取采购明细详情时出错: {e}')
        return jsonify({'error': '获取采购明细详情失败'}), 500
    finally:
        cursor.close()
        conn.close()


@purchases_bp.route('/update_purchase_detail', methods=['POST'])
@role_required(['Admin', 'Warehouse'])
def update_purchase_detail():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '未提供输入数据'}), 400

        PDid = data.get('PDid')
        Pcount = data.get('Pcount')
        other = data.get('other', '')

        if not PDid or Pcount is None:
            return jsonify({'error': '缺少必填字段'}), 400

        try:
            Pcount = int(Pcount)
        except ValueError:
            return jsonify({'error': 'Pcount 必须是整数'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # 获取现有记录
        cursor.execute('SELECT Pid, Gid FROM tb_pay_detail WHERE PDid=%s', (PDid,))
        detail = cursor.fetchone()
        if not detail:
            return jsonify({'error': '采购明细记录不存在'}), 400

        Pid, Gid = detail

        # 获取 GPay
        cursor.execute('SELECT GPay FROM tb_good WHERE Gid=%s', (Gid,))
        good = cursor.fetchone()
        GPay = good[0]

        total = Pcount * GPay

        # 更新明细记录
        cursor.execute(
            'UPDATE tb_pay_detail SET Pcount=%s, GPay=%s, total=%s, other=%s WHERE PDid=%s',
            (Pcount, GPay, total, other, PDid)
        )

        # 更新采购主表的 Pcount 和 Ptotal
        cursor.execute('SELECT SUM(Pcount), SUM(total) FROM tb_pay_detail WHERE Pid=%s', (Pid,))
        sum_pcount, sum_total = cursor.fetchone()
        cursor.execute('UPDATE tb_pay_main SET Pcount=%s, Ptotal=%s WHERE Pid=%s', (sum_pcount, sum_total, Pid))

        conn.commit()

        return jsonify({'message': '成功更新采购明细记录'}), 200
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f'更新采购明细时出错: {e}')
        return jsonify({'error': '更新采购明细记录失败'}), 500
    finally:
        cursor.close()
        conn.close()


@purchases_bp.route('/delete_purchase_detail', methods=['POST'])
@role_required(['Admin', 'Warehouse'])
def delete_purchase_detail():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '未提供输入数据'}), 400

        PDid = data.get('PDid')
        if not PDid:
            return jsonify({'error': '缺少 PDid 参数'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # 获取对应的 Pid
        cursor.execute('SELECT Pid FROM tb_pay_detail WHERE PDid=%s', (PDid,))
        result = cursor.fetchone()
        if not result:
            return jsonify({'error': '采购明细记录不存在'}), 400
        Pid = result[0]

        # 删除采购明细记录
        cursor.execute('DELETE FROM tb_pay_detail WHERE PDid=%s', (PDid,))

        # 更新采购主表的 Pcount 和 Ptotal
        cursor.execute('SELECT SUM(Pcount), SUM(total) FROM tb_pay_detail WHERE Pid=%s', (Pid,))
        sum_result = cursor.fetchone()
        sum_pcount = sum_result[0] if sum_result[0] else 0
        sum_total = sum_result[1] if sum_result[1] else 0.0
        cursor.execute('UPDATE tb_pay_main SET Pcount=%s, Ptotal=%s WHERE Pid=%s', (sum_pcount, sum_total, Pid))

        conn.commit()

        return jsonify({'message': '成功删除采购明细记录'}), 200
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f'删除采购明细时出错: {e}')
        return jsonify({'error': '删除采购明细记录失败'}), 500
    finally:
        cursor.close()
        conn.close()


@purchases_bp.route('/export_purchases', methods=['GET'])
@role_required(['Admin', 'Warehouse'])
def export_purchases():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tb_pay_main')
        purchases_main = cursor.fetchall()

        cursor.execute('SELECT * FROM tb_pay_detail')
        purchases_detail = cursor.fetchall()

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
        encoded_output = io.BytesIO(output.getvalue().encode('utf-8-sig'))

        return send_file(
            encoded_output,
            mimetype='text/csv',
            download_name='purchases.csv',
            as_attachment=True
        )
    except Exception as e:
        current_app.logger.error(f'导出采购数据时出错: {e}')
        return jsonify({'error': '导出采购数据失败'}), 500
    finally:
        cursor.close()
        conn.close()


@purchases_bp.route('/search_purchases_main', methods=['GET'])
@role_required(['Admin', 'Warehouse'])
def search_purchases_main():
    try:
        eid = request.args.get('eid', '').lower()
        pdate = request.args.get('pdate', '').lower()

        query = 'SELECT * FROM tb_pay_main WHERE LOWER(Eid) LIKE %s AND LOWER(Pdate) LIKE %s'
        params = (f'%{eid}%', f'%{pdate}%')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        purchases_main = cursor.fetchall()

        purchases_main_list = [{
            'Pid': purchase[0],
            'Eid': purchase[1],
            'Pcount': purchase[2],
            'Ptotal': purchase[3],
            'Pdate': purchase[4],
            'other': purchase[5]
        } for purchase in purchases_main]

        return jsonify(purchases_main_list)
    except Exception as e:
        current_app.logger.error(f'搜索采购主表时出错: {e}')
        return jsonify({'error': '搜索采购主表失败'}), 500
    finally:
        cursor.close()
        conn.close()


@purchases_bp.route('/search_purchases_detail', methods=['GET'])
@role_required(['Admin', 'Warehouse'])
def search_purchases_detail():
    try:
        pid = request.args.get('pid', '').lower()
        gid = request.args.get('gid', '').lower()

        query = 'SELECT * FROM tb_pay_detail WHERE LOWER(Pid) LIKE %s AND LOWER(Gid) LIKE %s'
        params = (f'%{pid}%', f'%{gid}%')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        purchases_detail = cursor.fetchall()

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
    except Exception as e:
        current_app.logger.error(f'搜索采购明细时出错: {e}')
        return jsonify({'error': '搜索采购明细失败'}), 500
    finally:
        cursor.close()
        conn.close()


@purchases_bp.route('/get_goods', methods=['GET'])
@role_required(['Admin', 'Warehouse'])
def get_goods():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT Gid FROM tb_good')
        goods = cursor.fetchall()
        goods_list = [{'Gid': good[0]} for good in goods]
        return jsonify(goods_list)
    except Exception as e:
        current_app.logger.error(f'获取商品列表时出错: {e}')
        return jsonify({'error': '获取商品列表失败'}), 500
    finally:
        cursor.close()
        conn.close()


@purchases_bp.route('/get_good_price', methods=['GET'])
@role_required(['Admin', 'Warehouse'])
def get_good_price():
    try:
        Gid = request.args.get('Gid')
        if not Gid:
            return jsonify({'error': '缺少 Gid 参数'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT GPay FROM tb_good WHERE Gid=%s', (Gid,))
        result = cursor.fetchone()

        if result:
            return jsonify({'GPay': result[0]})
        else:
            return jsonify({'error': '未找到商品'}), 404
    except Exception as e:
        current_app.logger.error(f'获取商品价格时出错: {e}')
        return jsonify({'error': '获取商品价格失败'}), 500
    finally:
        cursor.close()
        conn.close()

@purchases_bp.route('/get_employees', methods=['GET'])
@role_required(['Admin', 'Warehouse'])
def get_employees():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT Eid FROM tb_employee')
        employees = cursor.fetchall()
        employee_list = [{'Eid': emp[0]} for emp in employees]
        return jsonify(employee_list)
    except Exception as e:
        current_app.logger.error(f'获取员工列表时出错: {e}')
        return jsonify({'error': '获取员工列表失败'}), 500
    finally:
        cursor.close()
        conn.close()
