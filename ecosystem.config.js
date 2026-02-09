module.exports = {
  apps: [{
    name: 'pybot',
    script: './bot.py',
    interpreter: './venv/bin/python',
    cwd: '/var/www/pybot',
    env: {
      PYTHONUNBUFFERED: '1'
    }
  }]
}