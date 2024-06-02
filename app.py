from turtle import pd
import re

from flask import Flask, render_template, send_from_directory

from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import jsonify

import pyecharts.options as opts
from pyecharts.charts import Line

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://test:test@localhost/pereformance_report'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'

db = SQLAlchemy(app)


class TestData(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    platform_id = db.Column(db.Integer, db.ForeignKey('platforms.id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    version_id = db.Column(db.BigInteger, db.ForeignKey('versions.id'), nullable=False)
    test_type = db.Column(db.String(50), nullable=False)
    test_category = db.Column(db.String(100), nullable=False)
    test_value = db.Column(db.Integer, nullable=False)
    value_unit = db.Column(db.String(10))


class Platform(db.Model):
    __tablename__ = 'platforms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

class Branch(db.Model):
    __tablename__ = 'branches'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    platform_id = db.Column(db.Integer, db.ForeignKey('platforms.id'), nullable=False)
    platform = db.relationship('Platform', back_populates='branches')

Platform.branches = db.relationship('Branch', order_by=Branch.id, back_populates='platform')

class Version(db.Model):
    __tablename__ = 'versions'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50),  unique=True, nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    platform_id = db.Column(db.Integer, db.ForeignKey('platforms.id'), nullable=False)

    def __repr__(self):
        return f"<Version {self.name}>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'branch_id': self.branch_id,
            'platform_id': self.platform_id
        }


@app.route('/platforms', methods=['GET'])
def get_platforms():
    platforms = Platform.query.order_by(Platform.id).all()
    return jsonify([{'id': p.id, 'name': p.name} for p in platforms])


@app.route('/platforms', methods=['POST'])
def create_platform():
    data = request.get_json()

    if not data or not data.get('name'):
        return jsonify({'message': 'Platform name is required'}), 400

    try:
        platform = Platform(name=data['name'])
        db.session.add(platform)
        db.session.commit()
        return jsonify({'message': 'Platform created successfully', 'id': platform.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating platform', 'error': str(e)}), 500

@app.route('/branches', methods=['POST'])
def create_branch():
    data = request.get_json()

    if not data or not data.get('name') or not data.get('platform_id'):
        return jsonify({'message': 'Branch name and platform_id are required'}), 400

    try:
        branch = Branch(name=data['name'], platform_id=data['platform_id'])
        db.session.add(branch)
        db.session.commit()
        return jsonify({'message': 'Branch created successfully', 'id': branch.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating branch', 'error': str(e)}), 500



@app.route('/branches', methods=['GET'])
def get_branches():
    platform_id = request.args.get('platform_id')
    if not platform_id:
        return jsonify({'error': 'Platform ID is required'}), 400

    branches = Branch.query.filter_by(platform_id=platform_id).all()
    return jsonify([{'id': b.id, 'name': b.name} for b in branches])



# 创建版本
@app.route('/versions', methods=['POST'])
def create_version():
    if request.is_json:
        data = request.get_json()
        version_name = data.get('name', None)
        branch_id = data.get('branch_id')
        platform_id = data.get('platform_id')

        if  not branch_id:
            return jsonify({'error': 'branch ID are required'}), 400
        if  not platform_id:
            return jsonify({'error': 'platform ID are required'}), 400
        if  not version_name:
            return jsonify({'error': 'version_name  are required'}), 400

            # 检查平台是否存在
        platform = Platform.query.get(platform_id)
        if not platform:
            return jsonify({'error': '平台不存在'}), 400

        # 检查分支是否存在并且属于指定的平台
        branch = Branch.query.filter_by(id=branch_id, platform_id=platform_id).first()
        if not branch:
            return jsonify({'error': '分支不存在或不属于指定的平台'}), 400

        if version_name:
            # 检查版本是否已存在
            existing_version = Version.query.filter_by(name=version_name).first()
            if existing_version:
                return jsonify({"error": "版本已存在"}), 400

            # 如果版本不存在，则创建新版本
            # 创建新版本
            new_version = Version(name=version_name, branch_id=branch_id,platform_id = platform_id)
            db.session.add(new_version)
            db.session.commit()
            return jsonify(new_version.to_dict()), 201
        else:
            return jsonify({"error": "无效的输入"}), 400
    else:
        return jsonify({"error": "无效的输入格式，期望为 JSON"}), 400

# 查询所有版本
@app.route('/versions', methods=['GET'])
def get_versions():
    branch_id = request.args.get('branch_id')
    if branch_id:
        versions = Version.query.filter_by(branch_id=branch_id).order_by(Version.id).all()
    else:
        versions = Version.query.distinct(Version.name).order_by(Version.id).all()

    result = [{"name": data.name} for data in versions]

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

    test_data = query.order_by(TestData.version).all()
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

@app.route('/create_platform', methods=['GET'])
def create_platform_page():
    return render_template('create_platform.html')

@app.route('/create_branch', methods=['GET'])
def create_branch_page():
    return render_template('create_branch.html')


@app.route('/upload_data', methods=['POST'])
def upload_data():
    file = request.files['file']
    text = file.read().decode('utf-8')
    lines = text.split('\n')

    platform_id = request.form.get('platform')
    branch_id = request.form.get('branch')
    version_id = request.form.get('version')
    test_type = request.form.get('test_type')

    # Step 1: 删除旧的数据
    query = db.session.query(TestData)
    filters = []
    if platform_id:
        filters.append(TestData.platform_id == platform_id)
    if branch_id:
        filters.append(TestData.branch_id == branch_id)
    if test_type:
        filters.append(TestData.test_type.ilike(test_type))
    if version_id:
        filters.append(TestData.version_id == version_id)

    if filters:
        query = query.filter(*filters)
        query.delete(synchronize_session=False)

    db.session.commit()  # 提交删除的更改

    testdata_list = []
    for line in lines:
        match = re.match(r"(.*)\s+([\d\.]+)(.*)", line)
        if match:
            category, test_value, unit = match.groups()
            testdata = TestData(test_category=category,
                                test_value=test_value,
                                value_unit=unit,
                                platform_id=platform_id,
                                branch_id=branch_id,
                                test_type=test_type,
                                version_id=version_id)
            testdata_list.append(testdata)
        else:
            print(line)


    if testdata_list:
        db.session.add_all(testdata_list)

    db.session.commit()  # 提交新的数据

    return jsonify({'message': '数据上传成功'})


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
