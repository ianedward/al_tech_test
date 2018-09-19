from __future__ import absolute_import
import falcon


def _issue_to_json(issue):

    return {
        'id': issue.id,
        'title': issue.title,
        'description': issue.description,
        'opened': issue.opened.isoformat() if issue.opened else None,
        'closed': issue.closed if issue.closed else None,

    }


class IssuesResource(object):
    def __init__(self, repo):
        self._repo = repo

    def on_get(self, req, resp):

        try:
            with self._repo.open() as repo:
                issue_list = repo.issues.list_issues()
                resp.media = {
                    'issues': [_issue_to_json(issue) for issue in issue_list]
                }
                resp.status = falcon.HTTP_200
        except IOError:
            raise falcon.HTTPNotFound()

    def on_post(self, req, resp):

        try:
            with self._repo.open() as repo:
                new_issue = req.media

                repo.issues.create_issue(
                    new_issue['title'],
                    new_issue['descriptionText'],
                    new_issue['closedDate']
                )
                resp.status = falcon.HTTP_201
        except IOError:
            raise falcon.HTTP_400


class IssueResource(object):
    def __init__(self, repo):
        self._repo = repo

    def on_get(self, req, resp, issue_id):
        try:
            with self._repo.open() as repo:
                issue = repo.issues.fetch_issue(int(issue_id))
                resp.media = _issue_to_json(issue)
                resp.status = falcon.HTTP_200
        except IOError:
            raise falcon.HTTPNotFound()

    def on_put(self, req, resp, issue_id):
        try:
            with self._repo.open() as repo:
                update = req.media
                repo.issues.update_issue(issue_id, **update)
                resp.status = falcon.HTTP_204
        except IOError:
            raise falcon.HTTP_400


class UserResource(object):
    def __init__(self, repo):
        self._repo = repo

    # def on_get(self, req, resp):
    #     try:
    #         with self._repo.open() as repo:
    #             # user_list = repo.users.fetch_users()
    #             issue_list = repo.users.fetch_users()
    #             print issue_list
    #             resp.media = {
    #                 'issues': 'Plenty Issues'
    #             }
    #             # resp.status = falcon.HTTP_200
    #     except IOError:
    #         raise falcon.HTTPNotFound()

    def on_post(self, req, resp):
        try:
            with self._repo.open() as repo:
                new_user = req.media

                repo.users.register_user(
                    new_user['user'],
                    new_user['password']
                )
                resp.status = falcon.HTTP_201
        except IOError:
            raise falcon.HTTP_400
