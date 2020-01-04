from flask import jsonify


def success_response(data, status=200):
    """
    Успешный ответ от сервера
    :param data: данные
    :param status: http status
    :return:
    """
    return jsonify({'result': data}), status


def error_response(message, status=500):
    """
    Ответ с ошибкой
    :param message: текст ошибки
    :param status: http status
    :return:
    """
    return jsonify({'message': message}), status
