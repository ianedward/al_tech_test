const m = require('mithril')

class IssuesList {
  constructor(vnode) {
    this.model = vnode.attrs.model
  }
  oninit() {
    this.model.loadIssues()
  }
  view() {
    return m('table.table', [
      m('thead', [
        m('th', 'title'),
        m('th', 'opened'),
        m('th', 'closed')
      ]),
      m('tbody', [
        this.model.list.map(item =>
          m('tr', [
            m('td.title-cell', m("a", {href: `/issues/${item.id}`, oncreate: m.route.link}, item.title)),
            m('td.opened-cell', item.opened),
            m('td.closed-cell', item.closed)
          ])
        )
      ])
    ])
  }
}


class ViewIssue {
  constructor(vnode) {
    this.model = vnode.attrs.model
    this.issueId = vnode.attrs.issueId
  }
  oninit() {
    this.model.loadIssue(this.issueId)
  }
  view() {
    let detail = this.model.issues[this.issueId]
    return detail
    ? m('div',[
        m('.row', [
          m('h1.col-sm-11', detail.title),
          m('.col-sm-1',
            m(
              'a.btn.btn-primary',
              {href: `/issues/${this.issueId}/edit`, oncreate: m.route.link},
              'Edit'
            )
          )
        ]),
        m('dl.row', [
          m('dt.col-sm-3', 'Opened'),
          m('dd.col-sm-3', detail.opened),
          m('dt.col-sm-3', 'Closed'),
          m('dd.col-sm-3', detail.closed),
        ]),
        m('h2', 'Description'),
        m('p.description', detail.description)
      ]
    )
    : m('.alert.alert-info', 'Loading')
  }
}

class EditIssue {
  constructor(vnode) {
    this.model = vnode.attrs.model
    this.issueId = vnode.attrs.issueId
  }
  async oninit() {
    await this.model.loadIssue(this.issueId)
  }
  view() {
    let issue = this.model.issues[this.issueId]
    return issue
    ? m(IssueEditor, {
      title: issue.title,
      descriptionText: issue.description,
      closedDate: issue.closed,
      onSubmit: async (fields) => {
        await this.model.updateIssue(this.issueId, fields)
        m.route.set(`/issues/${this.issueId}`)
        m.redraw()
      }
    })
    :m('.alert.alert-info', 'Loading')
  }
}

class CreateIssue {
  constructor(vnode) {
    this.model = vnode.attrs.model
  }
  view() {
    return m(IssueEditor, {
      title: '',
      descriptionText: '',
      closedDate: '',
      onSubmit: async ({descriptionText, title, closedDate}) => {
        await this.model.createIssue({descriptionText: descriptionText, title: title, closedDate: closedDate})
        m.route.set(`/issues`)
        m.redraw()
      }
    })
  }
}

class CreateUser {
  constructor(vnode) {
    this.model = vnode.attrs.model
  }
  view() {
    return m(UserEditor, {
      user: '',
      password: '',
      onSubmit: async ({password, user}) => {
        await this.model.createUser({password: password, user: user})
        m.route.set(`/issues`)
        m.redraw()
      }
    })
  }
}


class UserEditor {
  constructor(vnode) {
    this.user = vnode.attrs.user
    this.password = vnode.attrs.password
    this.onSubmit = vnode.attrs.onSubmit
    }
  view() {
  return m('form', {onsubmit: e => this.onSubmit({user: this.user, password: this.password})},
        m("h1", "Register"),
        m('.form-group', [
              m('label', {'for': 'user-input'}, 'Username'),
              m('input[type=email][placeholder=user@gmail.com][required].form-control#title-input', {value: this.user, oninput: (e) => {this.user = e.target.value}})
        ]),
        m('.form-group', [
              m('label', {'for': 'password-input'}, 'Password'),
              m('input[type=password][placeholder=password][required].form-control#password-input', {value: this.password, oninput: (e) => {this.password = e.target.value}})
        ]),
        m('button.btn.btn-primary#save-button', {type: 'submit'}, 'register')

  )
  }
}



class IssueEditor {
  constructor(vnode) {
    this.title = vnode.attrs.title
    this.descriptionText = vnode.attrs.descriptionText
    this.closedDate = vnode.attrs.closedDate
    this.onSubmit = vnode.attrs.onSubmit
  }

  view() {
    return m('form', {onsubmit: e => this.onSubmit({title: this.title, descriptionText: this.descriptionText, closedDate: this.closedDate})}, [
      m('.form-group', [
        m('label', {'for': 'title-input'}, 'Issue Title'),
        m('input.form-control#title-input', {value: this.title, oninput: (e) => {this.title = e.target.value}})
      ]),
      m('.form-group', [
        m('label', {'for': 'description-input'}, 'Description'),
        m('textarea.form-control#description-input', {value: this.descriptionText, oninput: (e) => {this.descriptionText = e.target.value}})
      ]),
      m('.form-group', [
        m('label', {'for': 'open-close-input'}, 'Issue Tracker'),
        m('input.[type=date]form-control#open-close-input', {value: this.closedDate, oninput: (e) => {this.closedDate = e.target.value}})
        ]),
      m('button.btn.btn-primary#save-button', {type: 'submit'}, 'Save')
    ])
  }
}

const ToolbarContainer = {
  view(vnode) {
    return m('div', [
      m('nav.navbar.navbar-expand-lg.navbar-light.bg-light', [
        m('a.navbar-brand', {href: '/issues', oncreate: m.route.link}, 'Bug Tracker'),
        m('.collapse.navbar-collapse', [
          m('ul.navbar-nav', [
            m('li.nav-item', [
              m('a.nav-link', {href: '/issues/create', oncreate: m.route.link}, 'Create')
            ])
          ])
        ]),
        m('.navbar-nav.navbar-right', [
          m('ul.navbar-nav', [
            m('li.nav-item', [
             m('a.nav-link.justify-content-end', {href: '/login', oncreate: m.route.link}, 'Login')
             ])
           ])
         ]),
         m('.navbar-nav.navbar-right', [
           m('ul.navbar-nav', [
             m('li.nav-item', [
              m('a.nav-link.justify-content-end', {href: '/register', oncreate: m.route.link}, 'Register')
              ])
            ])
          ])
      ]),
      m('.container', vnode.children)
    ])
  }
}

module.exports = {IssuesList, ViewIssue, EditIssue, CreateIssue, IssueEditor, UserEditor, CreateUser, ToolbarContainer}
