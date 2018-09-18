from __future__ import absolute_import
import argparse
import falcon
import os

import json
from .resources import IssueResource, IssuesResource, UserResource
from .models import Repository

class ErrorHandler:
    @staticmethod
    def http(ex, req, resp, params):
        description = ('Sorry, Page Requested Not Found.')
        resp.status = falcon.HTTP_404
        resp.data = "Page Not Found"

    @staticmethod
    def unexpected(ex, req, resp, params):
        raise falcon.HTTPInternalServerError()


# class UserResource(object):
#     def __init__(self, repo):
#         self._repo = repo
#
#     def on_get(self, req, resp, user_id):
#         print "USER RESOURCES REQUESTED ____________________----------------_________________________"
#         try:
#             with self._repo.open() as repo:
#                 resp.status = falcon.HTTP_200
#                 print "USER RESOURCES REQUESTED ____________________----------------_________________________"
#         except IOError:
#             print "PAGE NOT FOUND AT ALL"
#             raise falcon.HTTPNotFound
#
#     def on_post(self, req, resp, user_id):
#         print "USER RESOURCES REQUESTED ____________________----------------_________________________"
#
#         with self._repo.open() as repo:
#             new_user = req.media
#             new_user_id = repo.users.register_user(
#                 new_user['user'],
#                 new_user['password']
#             )
#             resp.status = falcon.HTTP_200
#             print "USER RESOURCES REQUESTED ____________________----------------_________________________"
#         raise falcon.HTTPSeeOther('/login/{}'.format(new_user_id))


# class IssuedResource(object):
#     def __init__(self, repo):
#         self._repo = repo
#
#     def on_get(self, req, resp):
#         print " ISSUED  __________--------------------________________"
#         try:
#             with self._repo.open() as repo:
#                 # user_list = repo.users.fetch_users()
#                 issue_list = repo.users.fetch_users()
#                 print issue_list
#                 resp.media = {
#                     'issues': 'Plenty Issues'
#                 }
#                 # resp.status = falcon.HTTP_200
#         except IOError:
#             raise falcon.HTTPNotFound()
#
#     def on_post(self, req, resp):
#         print " POST ISSUED _____________----------------______________________"
#         with self._repo.open() as repo:
#             new_issue = req.media
#             new_id = repo.issues.create_issue(
#                 new_issue['title'],
#                 new_issue['description']
#             )
#         raise falcon.HTTPSeeOther('/issues/{}'.format(new_id))


def _index_middleware(app):
    def handler(environ, start_response):
        a = 0
        a += 1
        print a
        if environ['PATH_INFO'] == '/':
            environ['PATH_INFO'] = '/index.html'
        return app(environ, start_response)
    return handler


def make_api(database_location, migrate_database=True):
    api = falcon.API()
    api.add_error_handler(Exception, ErrorHandler.unexpected)
    api.add_error_handler(falcon.HTTPError, ErrorHandler.http)
    api.add_error_handler(falcon.HTTPStatus, ErrorHandler.http)
    repo = Repository(database_location)

    if migrate_database:
        repo.migrate_database()
    images = UserResource(repo)
    print images

    api.add_route('/issues', IssuesResource(repo))
    api.add_route('/issues/{issue_id}', IssueResource(repo))
    # api.add_route('/login', images)
    api.add_route('/register', UserResource(repo))
    print "make API **************************"
    static_dir = os.path.abspath(os.path.join(__file__, '..', '..', 'dist'))
    api.add_static_route('/', static_dir)
    return _index_middleware(api)


if __name__ == '__main__':
    from werkzeug.serving import make_server

    parser = argparse.ArgumentParser(description="Run a bug tracker server")
    parser.add_argument('--interface', default='0.0.0.0',
                        help="Interface to bind to")
    parser.add_argument('--port', default=8640,
                        help="Port to listen on")
    parser.add_argument('--database-location',
                        default=os.path.join(
                            os.path.dirname(__file__), '..', 'database.db'
                        ), help="Where to store the database")
    parser.add_argument('--no-database-migrations', action='store_true',
                        help="Do not perform database migrations")
    parser.add_argument('--clean', action='store_true',
                        help="Delete the database and start from clean")
    args = parser.parse_args()
    if args.clean:
        os.remove(args.database_location)

    api = make_api(args.database_location, not args.no_database_migrations)
    httpd = make_server(args.interface, args.port, api)
    print "Serving on {args.interface}:{args.port}".format(args=args)
    httpd.serve_forever()
