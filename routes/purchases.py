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

# Main management page, accessible by Admin and Warehouse roles
@purchases_bp.route('/main_management')
@role_required(['Admin', 'Warehouse'])
def main_management():
    return render_template('main_management.html')


# Detail management page, accessible by Admin and Warehouse roles
@purchases_bp.route('/detail_management')
@role_required(['Admin', 'Warehouse'])
def detail_management():
    return render_template('detail_management.html')


@purchases_bp.route('/add_purchase_main', methods=['POST'])
@role_required(['Admin', 'Warehouse'])
def add_purchase_main():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    Eid = data.get('Eid')
    other = data.get('other', '')
    Pcount = 0  # Initial value
    Ptotal = 0.0  # Initial value

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if employee exists
        cursor.execute('SELECT * FROM tb_employee WHERE Eid=%s', (Eid,))
        employee = cursor.fetchone()
        if not employee:
            return jsonify({'error': 'Employee ID does not exist'}), 400

        # Generate new Pid
        cursor.execute('SELECT MAX(Pid) FROM tb_pay_main')
        max_pid = cursor.fetchone()[0]
        new_pid = (max_pid or 0) + 1

        # Get latest Pdate and add one day
        cursor.execute('SELECT MAX(Pdate) FROM tb_pay_main')
        max_pdate = cursor.fetchone()[0]
        if max_pdate:
            latest_date = datetime.datetime.strptime(max_pdate, '%Y-%m-%d').date()
            new_pdate = latest_date + datetime.timedelta(days=1)
        else:
            new_pdate = datetime.date.today()
        Pdate = new_pdate.strftime('%Y-%m-%d')

        # Insert the new record
        cursor.execute(
            'INSERT INTO tb_pay_main (Pid, Eid, Pcount, Ptotal, Pdate, other) '
            'VALUES (%s, %s, %s, %s, %s, %s)',
            (new_pid, Eid, Pcount, Ptotal, Pdate, other)
        )
        conn.commit()
        return jsonify({'message': 'Purchase main record added successfully', 'Pid': new_pid}), 201
    except Exception as e:
        current_app.logger.error(f'Error adding purchase main: {e}')
        conn.rollback()
        return jsonify({'error': 'Failed to add purchase main record'}), 500
    finally:
        conn.close()


@purchases_bp.route('/get_purchases_main', methods=['GET'])
@role_required(['Admin', 'Warehouse'])
def get_purchases_main():
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
@role_required(['Admin', 'Warehouse'])
def get_purchase_main():
    Pid = request.args.get('Pid')
    if not Pid:
        return jsonify({'error': 'Missing Pid parameter'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_pay_main WHERE Pid=%s', (Pid,))
    purchase_main = cursor.fetchone()
    conn.close()

    if not purchase_main:
        return jsonify({'error': 'Purchase main record not found'}), 404

    purchase_main_dict = {
        'Pid': purchase_main[0],
        'Eid': purchase_main[1],
        'Pcount': purchase_main[2],
        'Ptotal': purchase_main[3],
        'Pdate': purchase_main[4],
        'other': purchase_main[5]
    }

    return jsonify(purchase_main_dict)


@purchases_bp.route('/update_purchase_main', methods=['PUT'])
@role_required(['Admin', 'Warehouse'])
def update_purchase_main():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    Pid = data.get('Pid')
    Eid = data.get('Eid')
    Pdate = data.get('Pdate')
    other = data.get('other', '')

    if not Pid or not Eid or not Pdate:
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if employee exists
        cursor.execute('SELECT * FROM tb_employee WHERE Eid=%s', (Eid,))
        employee = cursor.fetchone()
        if not employee:
            return jsonify({'error': 'Employee ID does not exist'}), 400

        # Update only editable fields
        cursor.execute(
            'UPDATE tb_pay_main SET Eid=%s, Pdate=%s, other=%s WHERE Pid=%s',
            (Eid, Pdate, other, Pid)
        )
        conn.commit()
        return jsonify({'message': 'Purchase main record updated successfully'}), 200
    except Exception as e:
        current_app.logger.error(f'Error updating purchase main: {e}')
        conn.rollback()
        return jsonify({'error': 'Failed to update purchase main record'}), 500
    finally:
        conn.close()


@purchases_bp.route('/delete_purchase_main', methods=['DELETE'])
@role_required(['Admin', 'Warehouse'])
def delete_purchase_main():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    Pid = data.get('Pid')

    if not Pid:
        return jsonify({'error': 'Missing Pid parameter'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Delete the purchase main record and cascade delete related details
        cursor.execute('DELETE FROM tb_pay_main WHERE Pid=%s', (Pid,))
        conn.commit()
        return jsonify({'message': 'Purchase main record deleted successfully'}), 200
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f'Error deleting purchase main: {e}')
        return jsonify({'error': 'Failed to delete purchase main record'}), 500
    finally:
        conn.close()


@purchases_bp.route('/add_purchase_detail', methods=['POST'])
@role_required(['Admin', 'Warehouse'])
def add_purchase_detail():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    Pid = data.get('Pid')
    Gid = data.get('Gid')
    Pcount = data.get('Pcount')
    other = data.get('other', '')

    if not Pid or not Gid or not Pcount:
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if purchase main exists
        cursor.execute('SELECT * FROM tb_pay_main WHERE Pid=%s', (Pid,))
        purchase_main = cursor.fetchone()
        if not purchase_main:
            return jsonify({'error': 'Purchase main record does not exist'}), 400

        # Check if good exists and get GPay
        cursor.execute('SELECT GPay FROM tb_good WHERE Gid=%s', (Gid,))
        good = cursor.fetchone()
        if not good:
            return jsonify({'error': 'Good ID does not exist'}), 400
        GPay = good[0]

        total = Pcount * GPay

        # Generate new PDid
        cursor.execute('SELECT MAX(PDid) FROM tb_pay_detail')
        max_pdid = cursor.fetchone()[0]
        new_pdid = (max_pdid or 0) + 1

        # Insert the new detail record
        cursor.execute(
            'INSERT INTO tb_pay_detail (PDid, Pid, Gid, Pcount, GPay, total, other) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (new_pdid, Pid, Gid, Pcount, GPay, total, other)
        )
        conn.commit()
        return jsonify({'message': 'Purchase detail record added successfully', 'PDid': new_pdid}), 201
    except Exception as e:
        current_app.logger.error(f'Error adding purchase detail: {e}')
        conn.rollback()
        return jsonify({'error': 'Failed to add purchase detail record'}), 500
    finally:
        conn.close()


@purchases_bp.route('/get_purchases_detail', methods=['GET'])
@role_required(['Admin', 'Warehouse'])
def get_purchases_detail():
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
@role_required(['Admin', 'Warehouse'])
def get_purchase_detail():
    PDid = request.args.get('PDid')
    if not PDid:
        return jsonify({'error': 'Missing PDid parameter'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_pay_detail WHERE PDid=%s', (PDid,))
    purchase_detail = cursor.fetchone()
    conn.close()

    if not purchase_detail:
        return jsonify({'error': 'Purchase detail record not found'}), 404

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


@purchases_bp.route('/update_purchase_detail', methods=['PUT'])
@role_required(['Admin', 'Warehouse'])
def update_purchase_detail():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    PDid = data.get('PDid')
    Pcount = data.get('Pcount')
    other = data.get('other', '')

    if not PDid or not Pcount:
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Fetch existing record
        cursor.execute('SELECT Pid, Gid FROM tb_pay_detail WHERE PDid=%s', (PDid,))
        detail = cursor.fetchone()
        if not detail:
            return jsonify({'error': 'Purchase detail record does not exist'}), 400

        Pid, Gid = detail

        # Get GPay from tb_good
        cursor.execute('SELECT GPay FROM tb_good WHERE Gid=%s', (Gid,))
        good = cursor.fetchone()
        GPay = good[0]

        total = Pcount * GPay

        # Update the detail record
        cursor.execute(
            'UPDATE tb_pay_detail SET Pcount=%s, GPay=%s, total=%s, other=%s WHERE PDid=%s',
            (Pcount, GPay, total, other, PDid)
        )
        conn.commit()
        return jsonify({'message': 'Purchase detail record updated successfully'}), 200
    except Exception as e:
        current_app.logger.error(f'Error updating purchase detail: {e}')
        conn.rollback()
        return jsonify({'error': 'Failed to update purchase detail record'}), 500
    finally:
        conn.close()


@purchases_bp.route('/delete_purchase_detail', methods=['DELETE'])
@role_required(['Admin', 'Warehouse'])
def delete_purchase_detail():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    PDid = data.get('PDid')
    if not PDid:
        return jsonify({'error': 'Missing PDid parameter'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM tb_pay_detail WHERE PDid=%s', (PDid,))
        conn.commit()
        return jsonify({'message': 'Purchase detail record deleted successfully'}), 200
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f'Error deleting purchase detail: {e}')
        return jsonify({'error': 'Failed to delete purchase detail record'}), 500
    finally:
        conn.close()


@purchases_bp.route('/export_purchases', methods=['GET'])
@role_required(['Admin', 'Warehouse'])
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

    return send_file(
        encoded_output,
        mimetype='text/csv',
        download_name='purchases.csv',
        as_attachment=True
    )


@purchases_bp.route('/search_purchases_main', methods=['GET'])
@role_required(['Admin', 'Warehouse'])
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
@role_required(['Admin', 'Warehouse'])
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


@purchases_bp.route('/get_goods', methods=['GET'])
@role_required(['Admin', 'Warehouse'])
def get_goods():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT Gid FROM tb_good')
    goods = cursor.fetchall()
    conn.close()
    goods_list = [{'Gid': good[0]} for good in goods]
    return jsonify(goods_list)


@purchases_bp.route('/get_good_price', methods=['GET'])
@role_required(['Admin', 'Warehouse'])
def get_good_price():
    Gid = request.args.get('Gid')
    if not Gid:
        return jsonify({'error': 'Missing Gid parameter'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT GPay FROM tb_good WHERE Gid=%s', (Gid,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return jsonify({'GPay': result[0]})
    else:
        return jsonify({'error': 'Good not found'}), 404


@purchases_bp.route('/get_latest_pdate', methods=['GET'])
@role_required(['Admin', 'Warehouse'])
def get_latest_pdate():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(Pdate) FROM tb_pay_main')
    max_pdate = cursor.fetchone()[0]
    if max_pdate:
        latest_date = datetime.datetime.strptime(max_pdate, '%Y-%m-%d').date()
        new_pdate = (latest_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        new_pdate = datetime.date.today().strftime('%Y-%m-%d')
    conn.close()
    return jsonify({'new_pdate': new_pdate})
