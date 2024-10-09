# app.py
from flask import Flask, redirect, url_for
from config import db_config, secret_key
from auth import auth_bp
from routes.customers import customers_bp
from routes.employees import employees_bp
from routes.goods import goods_bp
from routes.purchases import purchases_bp
from routes.stats import stats_bp
import logging

app = Flask(__name__)

# Setting secret_key
app.secret_key = secret_key

app.config['db_config'] = db_config
# 删除 redis_config 相关配置
# app.config['redis_config'] = redis_config

# Registering Blueprints
app.logger.info("Registering blueprints...")
app.register_blueprint(auth_bp)
app.register_blueprint(customers_bp)
app.register_blueprint(employees_bp)
app.register_blueprint(goods_bp)
app.register_blueprint(purchases_bp)
app.register_blueprint(stats_bp)


# Redirect root to /login
@app.route('/')
def index():
    app.logger.info("Redirecting to login page...")
    return redirect(url_for('auth.login'))


if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)
    app.run(debug=True)
