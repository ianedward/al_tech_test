require('babel-polyfill')
const m = require('mithril')
const {IssuesList, ViewIssue, CreateIssue, EditIssue, ToolbarContainer, CreateUser} = require('./views')
const {IssuesModel} = require('./viewmodels')
const {UserModel} = require('./viewmodels')

const issuesModel = new IssuesModel()
const userModel = new UserModel()

m.route(document.body, '/issues', {
  '/register': {
    render(vnode) {
       return m(ToolbarContainer, m(CreateUser, {model: userModel}))
    }
  },

  '/issues': {
    render(vnode) {
      return m(ToolbarContainer, m(IssuesList, {model: issuesModel}))
    }
  },
  '/issues/create': {
    render(vnode) {
      return m(ToolbarContainer, m(CreateIssue, {model: issuesModel}))
    }
  },
  '/issues/:issueId': {
    render(vnode) {
      return m(
        ToolbarContainer,
        (vnode.attrs.issueId === 'new')
        ? m(CreateIssue, {model: issuesModel})
        : m(ViewIssue, {model: issuesModel, issueId: vnode.attrs.issueId}))
    }
  },
  '/issues/:issueId/edit': {
    render(vnode) {
      return m(ToolbarContainer, m(EditIssue, {model: issuesModel, issueId: vnode.attrs.issueId}))
    }
  }
})
