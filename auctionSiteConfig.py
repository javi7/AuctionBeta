import web

import urlHandlers
import apiHandlers
import ajaxHandlers

urls = (
	'/', 'urlHandlers.Home',
	'/bid', 'urlHandlers.Bid',
	'/api/bid', 'apiHandlers.Bid',
	'/ajax/logout', 'ajaxHandlers.Reset',
	'/ajax/login', 'ajaxHandlers.Login',
	'/team', 'urlHandlers.Team',
	'/api/keep', 'apiHandlers.Keep',
	'/ajax/register', 'ajaxHandlers.Register',
	'/rules', 'urlHandlers.Rules',
	'/account', 'urlHandlers.Account',
	'/ajax/changeaccount', 'ajaxHandlers.ChangeAccount',
	'/scoreboard', 'urlHandlers.Scoreboard',
	'/standings', 'urlHandlers.Standings',
	'/game/([1-9][0-9]*)', 'urlHandlers.Game'
)

app = web.application(urls, globals())

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'loggedin': False})
    web.config._session = session
else:
    session = web.config._session

if __name__ == "__main__":
    app.run()
