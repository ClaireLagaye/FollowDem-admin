from pypnusershub import routes as fnauth
from flask import (Blueprint, jsonify, request)
from models import Device,DeviceType, db
import traceback
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, desc, or_

devices = Blueprint('devices', __name__)


@devices.route('/api/devices', methods=['GET'])
@fnauth.check_auth(4)
def get_Devices():
    try:
        key = request.args.get("key")
        devices = []
        if key:
            devices = Device.query. \
                filter(or_(Device.reference.ilike("%" + key + "%"))). \
                order_by(desc(Device.id)). \
                all()
        else:
            devices = Device.query. \
                order_by(desc(Device.id)). \
                all()
        return jsonify([Device.json() for Device in devices])
    except Exception:
        traceback.print_exc()
        return jsonify(error='Invalid JSON.'), 400

@devices.route('/api/devices/<int:id>', methods=['GET'])
@fnauth.check_auth(4)
def get_device_by_id(id=id):
    try:
        device = Device.query.get(id)
        if device:
            return jsonify(device.json())
        else:
            return 'error not found'
    except Exception:
        traceback.print_exc()
        return jsonify(error='Invalid JSON.'), 400


@devices.route('/api/devices', methods=['POST'])
@fnauth.check_auth(4)
def save_Devices():
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
@fnauth.check_auth(4)
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
        id = int(payload['id'])
        del payload['id']
        db.session.query(Device).filter(Device.id == id).update(payload)
        db.session.commit()
        return jsonify(device.json())
    except (IntegrityError, Exception) as e:
        traceback.print_exc()
        db.session.rollback()


@devices.route('/api/devices', methods=['DELETE'])
@fnauth.check_auth(4)
def delete_Devices():
    try:
        ids = request.args.getlist('id[]')
        for id in ids:
            db.session.query(Device).filter(Device.id == int(id)).delete()
            db.session.commit()
        return jsonify('success'), 200
    except Exception:
        traceback.print_exc()
        return jsonify(error='Invalid JSON.'), 400


def devices_validate_required(device):
    errors = []
    for attr in ('reference', 'device_type_id'):
        if not device.get(attr, None):
            errors.append({
                'name': 'missing_attribute',
                'table': 'devices',
                'column': attr
            })
    reference = device.get('reference').lower()
    reference = reference.strip()
    device_exist = Device.query.filter(Device.reference == reference).first()
    if (device_exist and (device_exist.json().get('id') != device.get('id'))):
          errors.append({
                'name': 'device_already_exists',
                'table': 'devices',
                'column': attr
            })
    if len(errors) >= 0:
        return {'errors': errors}

    return True
