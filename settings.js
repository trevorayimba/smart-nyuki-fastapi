// settings.js - basic minimal configuration
module.exports = {
  httpAdminRoot: '/admin',
  httpNodeRoot: '/',
  userDir: './data',
  flowFile: 'flows.json',
  flowFilePretty: true,
  logging: {
    console: {
      level: "info",
      metrics: false,
      audit: false
    }
  }
}
