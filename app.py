from turtle import pd
import re

from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import jsonify

import pyecharts.options as opts
from pyecharts.charts import Line

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/pereformance-report'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'

db = SQLAlchemy(app)


class TestData(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    platform = db.Column(db.String(50), nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    test_type = db.Column(db.String(50), nullable=False)
    version = db.Column(db.String(50), nullable=False)
    test_category = db.Column(db.String(100), nullable=False)
    test_value = db.Column(db.Integer, nullable=False)
    value_unit = db.Column(db.String(10))


@app.route('/get_report_data', methods=['GET'])
def get_test_data():
    platform = request.args.get('platform')
    branch = request.args.get('branch')
    test_type = request.args.get('test_type')
    version = request.args.get('version')

    test_data = TestData.query.filter_by(platform=platform, branch=branch, test_type=test_type, version=version).all()
    result = [{"category": data.test_category, "value": data.test_value} for data in test_data]

    return jsonify(result)


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/upload_data', methods=['POST'])
def upload_data():
    file = request.files['file']
    text = file.read().decode('utf-8')
    lines = text.split('\n')

    platform = request.form.get('platform')
    branch = request.form.get('branch')
    test_type = request.form.get('test_type')
    version = request.form.get('version')

    testdata_list = []
    for line in lines:
        match = re.match(r"([\w\s\-]+)\s+(\d+)(\w+)?", line)
        if match:
            category, test_value, unit = match.groups()
            testdata = TestData(test_category=category,
                                test_value=test_value,
                                value_unit=unit,
                                platform=platform,
                                branch=branch,
                                test_type=test_type,
                                version=version)

            testdata_list.append(testdata)

        else:
            pass

    if testdata_list is not None:
        db.session.add_all(testdata_list)
        db.session.commit()

    return '数据上传成功'


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
