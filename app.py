from turtle import pd
import re

from flask import Flask, render_template, send_from_directory

from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import jsonify

import pyecharts.options as opts
from pyecharts.charts import Line

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://test:test@localhost/pereformance-report'
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


class Version(db.Model):
    __tablename__ = 'versions'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Version {self.name}>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

# 创建版本
@app.route('/versions', methods=['POST'])
def create_version():
    if request.is_json:
        data = request.get_json()
        version_name = data.get('name', None)
        if version_name:
            new_version = Version(name=version_name)
            db.session.add(new_version)
            db.session.commit()
            return jsonify(new_version.to_dict()), 201
        else:
            return jsonify({"error": "Invalid input"}), 400
    else:
        return jsonify({"error": "Invalid input format, expected JSON"}), 400

# 查询所有版本
@app.route('/versions', methods=['GET'])
def get_versions():

    versions = db.session.query(Version.name).distinct().all()

    result = [{"name": data.name}
              for data in versions]

    return jsonify(result)

@app.route('/test_categories', methods=['GET'])
def get_test_items():
    test_categories = db.session.query(TestData.test_category).distinct().all()
    test_item_list = [category[0] for category in test_categories]  # 提取元组中的类别名称
    return jsonify(test_item_list)

@app.route('/get_report_data', methods=['GET'])
def get_test_data():
    platform = request.args.get('platform')
    branch = request.args.get('branch')
    test_type = request.args.get('test_type')
    version = request.args.get('version')
    testCategories = request.args.get('test_category')

    query = TestData.query

    # 假设 query 是您的查询对象
    if platform:
        query = query.filter(TestData.platform.ilike(f'%{platform}%'))
    if branch:
        query = query.filter(TestData.branch.ilike(f'%{branch}%'))
    if test_type:
        query = query.filter(TestData.test_type == test_type)
    if version:
        # 处理多个version，假设用逗号分隔
        version_list = version.split(',')
        query = query.filter(TestData.version.in_(version_list))
    if testCategories:
        # 处理多个 testCategories，假设用逗号分隔
        test_categories_list = testCategories.split(',')
        query = query.filter(TestData.test_category.in_(test_categories_list))

    test_data = query.all()
    result = [{"category": data.test_category, "value": data.test_value, "version": data.version,
               "value_unit": data.value_unit
               }
              for data in test_data]
    return jsonify(result)


@app.route('/data_dashboard')
def data_dashboard():
    return render_template('data_dashboard.html')

@app.route('/data_upload')
def data_upload():
    return render_template('data_upload.html')

@app.route('/create_version')
def create_version_page():
    return render_template('create_version.html')


@app.route('/upload_data', methods=['POST'])
def upload_data():
    file = request.files['file']
    text = file.read().decode('utf-8')
    lines = text.split('\n')

    platform = request.form.get('platform')
    branch = request.form.get('branch')
    test_type = request.form.get('test_type')
    version = request.form.get('version')

    # Step 1: 删除旧的数据
    query = db.session.query(TestData)
    filters = []
    if platform:
        filters.append(TestData.platform.ilike(platform))
    if branch:
        filters.append(TestData.branch.ilike(branch))
    if test_type:
        filters.append(TestData.test_type.ilike(test_type))
    if version:
        filters.append(TestData.version.ilike(version))

    if filters:
        query = query.filter(*filters)
        query.delete(synchronize_session=False)

    query.delete(synchronize_session=False)

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
