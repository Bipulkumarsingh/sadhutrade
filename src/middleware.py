# import jwt
# from datetime import datetime
# from werkzeug.wrappers import Request, Response
# from util.main_logger import set_up_logging
# from src.response import ResponseData
#
# logger = set_up_logging()
# response = ResponseData()
#
#
# def token_validation(base_token, environ=None, socket=False):
#     try:
#         key, token = base_token.split()
#         decoded_token = jwt.decode(token, key, algorithms=['HS256'], options={"verify_signature": False})["userVo"]
#         if not socket:
#             environ['context'] = decoded_token  # Creating context key in environ dict
#             return True
#         return decoded_token
#     except Exception as ex:
#         logger.exception("Failed to decode token: %s", ex)
#         return False
#
#
# class AuthMiddleware:
#     def __init__(self, app):
#         self.app = app
#
#     def __call__(self, environ, start_response):
#         start_time = datetime.now()
#         request = Request(environ)
#         req_header = request.headers
#         token = req_header.get('Authorization')
#         response.HEADERS['Authorization'] = token
#         end_point = True if request.host != "askme-queue-service:8080" else False
#         if request.method == "POST":
#             if token is None and end_point:
#                 resp = Response(u'Authentication token required', mimetype='text/plain', status=401)
#                 return resp(environ, start_response)
#             elif not token_validation(token, environ) and end_point:
#                 logger.info("Token is not valid")
#                 resp = Response(u'Authentication token is not valid', mimetype='text/plain', status=401)
#                 return resp(environ, start_response)
#
#         def injecting_start_response(status, headers, exc_info=None):
#             end_time = datetime.now()
#             time_taken = (end_time - start_time).total_seconds() * 1000
#             headers.extend([('X-Time-Taken', f"{str(round(time_taken, 2))} ms"), ('SESSIONID', req_header.get('SESSIONID', "")),
#                             ('TRANSACTIONID', req_header.get('TRANSACTIONID', ""))])
#             return start_response(status, headers, exc_info)
#         return self.app(environ, injecting_start_response)
#
#         # # Every thing is fine and token is decoded
#         # return self.app(environ, start_response)
