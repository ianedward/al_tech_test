const m = require('mithril')

class IssuesModel {
  constructor() {
    this.issues = {}
  }
  async loadIssues() {
    let response = await m.request('/issues')
    console.log(response.issues)
    this.issues = {}
    for (let issue of response.issues) {
      console.log(issue)
      this.issues[issue.id] = issue
    }
    return this.issues
  }
  get list() {
    return Object.keys(this.issues).map(i => this.issues[i])
  }
  async loadIssue(issueId) {
    let response = await m.request(`/issues/${issueId}`)
    this.issues[issueId] = response
    return response
  }
  async updateIssue(issueId, fields) {
  var title = fields.title
  var desc = fields.descriptionText
  var closedt = fields.closedDate
  console.log(title)
  console.log(desc)
  console.log(closedt)
    await m.request({
      method: "PUT",
      url: `/issues/${issueId}`,
      data: fields
    })
    return await this.loadIssue(issueId)
  }
  async createIssue(fields) {
    await m.request({
      method: "POST",
      url: `/issues`,
      data: fields
    })

    return await this.loadIssues()
  }
}


class UserModel {
  constructor() {
  this.users = {}
  }

  async loadPage() {
    let response = await m.request('/register')
    console.log(response.users)
    this.users = {}
    for (let user of response.users) {
      this.users[user.id] = user
    }
    return this.users
  }

  async createUser(fields) {
    var user = fields.user
    var password = fields.password
    console.log(user)
    console.log(password)
    await m.request ({
      method: "POST",
      url: `/register`,
      data: fields
      }).then(function(response){
      console.log(response)})
    return await this.loadPage()
  }
}


module.exports = {IssuesModel, UserModel}
