from flask import Blueprint, jsonify, render_template, current_app
from db import get_db_connection

stats_bp = Blueprint('stats', __name__)


@stats_bp.route('/statistics')
def statistics():
    return render_template('statistics.html')


@stats_bp.route('/get_employee_statistics', methods=['GET'])
def get_employee_statistics():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_employee')
    employees = cursor.fetchall()
    conn.close()
    return jsonify(employees)


@stats_bp.route('/get_good_statistics', methods=['GET'])
def get_good_statistics():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_good')
    goods = cursor.fetchall()
    conn.close()
    return jsonify(goods)


@stats_bp.route('/get_purchase_statistics', methods=['GET'])
def get_purchase_statistics():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_pay_main')
    purchases_main = cursor.fetchall()

    cursor.execute('SELECT * FROM tb_pay_detail')
    purchases_detail = cursor.fetchall()
    conn.close()

    data = {'main': purchases_main, 'detail': purchases_detail}
    return jsonify(data)
