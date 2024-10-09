from flask import Blueprint, request, session, redirect, url_for, render_template, jsonify, flash  # Add jsonify
from db import get_db_connection
from functools import wraps

auth_bp = Blueprint('auth', __name__)


# 权限控制装饰器
def role_required(allowed_roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if 'role' not in session:
                return redirect(url_for('auth.login'))
            if session['role'] not in allowed_roles:
                flash("您没有权限访问此页面", "danger")
                return redirect(url_for('auth.dash_board'))
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


@auth_bp.route('/get_user_info', methods=['GET'])
def get_user_info():
    if 'username' in session and 'role' in session:
        return jsonify({
            'username': session['username'],  # 用户名
            'role': session['role']           # 用户权限
        })
    return jsonify({'error': '未登录'}), 401


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM admin WHERE username=%s AND password=%s', (username, password))
        admin = cursor.fetchone()
        conn.close()

        if admin:
            session['username'] = admin[1]  # 假设用户名在第一列
            session['role'] = admin[3]  # 假设角色在第四列
            return redirect(url_for('auth.dash_board'))  # 重定向到仪表盘
        else:
            # 使用 flash 存储错误信息
            flash('通行证或密码错误，请重试', 'danger')
            return redirect(url_for('auth.login'))  # 返回登录页面

    return render_template('login.html')


# 添加 dash_board 路由
@auth_bp.route('/dash_board')
def dash_board():
    return render_template('dash_board.html')  # 渲染仪表盘页面


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
