from flask import Blueprint, request, session, redirect, url_for, render_template, jsonify, flash, send_file
from db import get_db_connection
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string
from captcha.image import ImageCaptcha

auth_bp = Blueprint('auth', __name__)


# Permission Decorator
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
            'username': session['username'],
            'role': session['role']
        })
    return jsonify({'error': '未登录'}), 401


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        username = request.form['username'].strip()
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM admin WHERE username=%s AND role=%s', (username, role))
        admin = cursor.fetchone()
        conn.close()

        if admin and check_password_hash(admin[2], password):  # Password is in the third column
            session['username'] = admin[1]  # Username
            session['role'] = admin[3]  # Role
            return redirect(url_for('auth.dash_board'))  # Redirect to dashboard
        else:
            flash('通行证或密码错误，请重试', 'danger')
            return redirect(url_for('auth.login'))  # Return to login page

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        role = request.form['role']
        username = request.form['username'].strip()
        password = request.form['password']
        captcha = request.form['captcha'].strip()

        # Validate inputs
        errors = []
        if not username:
            errors.append('通行证不能为空。')
        if not password.strip():
            errors.append('密码不能是纯空格。')
        if len(password) < 8:
            errors.append('密码必须至少8个字符长。')
        if captcha.lower() != session.get('captcha', '').lower():
            errors.append('验证码不正确。')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return redirect(url_for('auth.register'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert the new user into the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute('SELECT id FROM admin WHERE username=%s', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            conn.close()
            flash('通行证已存在，请选择另一个。', 'danger')
            return redirect(url_for('auth.register'))

        try:
            cursor.execute(
                'INSERT INTO admin (username, password, role) VALUES (%s, %s, %s)',
                (username, hashed_password, role)
            )
            conn.commit()
            flash('注册成功，请登录。', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            conn.rollback()
            flash('注册失败，请重试。', 'danger')
        finally:
            conn.close()

    return render_template('register.html')


@auth_bp.route('/captcha')
def captcha():
    # 生成验证码文本
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    session['captcha'] = captcha_text

    # 生成验证码图片
    image = ImageCaptcha(width=280, height=90)
    data = image.generate(captcha_text)
    return send_file(data, mimetype='image/png')


@auth_bp.route('/dash_board')
def dash_board():
    return render_template('dash_board.html')  # Render the dashboard page


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
