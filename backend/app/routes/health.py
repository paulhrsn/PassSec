from flask import Blueprint, jsonify

#create blueprint for health-check endpoints
health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])