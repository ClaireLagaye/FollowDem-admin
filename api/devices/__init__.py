from flask import (Blueprint, jsonify, request)
from models import Device, db
import traceback
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, desc

devices = Blueprint('devices', __name__)

@devices.route('/api/devices', methods=['GET'])
def get_Devices():
    try:
        devices = Device.query.\
        order_by(desc(Device.id)). \
        all()
        return jsonify([ Device.json() for Device in devices ])
    except Exception:
        traceback.print_exc()
        return jsonify(error='Invalid JSON.'), 400

@devices.route('/api/devices', methods=['POST'])
def save_Devices():
    print("yes")
    try:
        payload = request.get_json()
    except Exception:
        return jsonify(error='Invalid JSON.')

    validation = devices_validate_required(payload)
    if validation['errors']:
        return jsonify(error={'name': 'invalid_model',
                              'errors': validation['errors']}), 400
    device = Device(**payload)
    try:
        db.session.add(device)
        db.session.commit()
        return jsonify(device.json())
    except (IntegrityError, Exception) as e:
        traceback.print_exc()
        db.session.rollback()

@devices.route('/api/devices', methods=['PATCH'])
def patch_Devices():
    try:
        payload = request.get_json()
    except Exception:
        return jsonify(error='Invalid JSON.')

    validation = devices_validate_required(payload)
    if validation['errors']:
        return jsonify(error={'name': 'invalid_model',
                              'errors': validation['errors']}), 400
    device = Device(**payload)
    try:
        Device.query.filter_by(id=Device.get('id')).update(device)
        return jsonify(Device.json())
    except (IntegrityError, Exception) as e:
        traceback.print_exc()
        db.session.rollback()

@devices.route('/api/devices', methods=['DELETE'])
def delete_Devices():
    try:
        ids = request.args.getlist('id[]')
        for id in ids:
            print(id)
            db.session.query(Device).filter(Device.id == int(id)).delete()
            db.session.commit()
        return jsonify('success'), 200
    except Exception:
        traceback.print_exc()
        return jsonify(error='Invalid JSON.'), 400


def devices_validate_required(Device):
    errors = []
    for attr in ('reference', 'comment', 'device_type_id'):
        if not Device.get(attr, None):
            errors.append({
                'name': 'missing_attribute',
                'table': 'devices',
                'column': attr
            })

    if len(errors) >= 0:
        return {'errors': errors}

    return True