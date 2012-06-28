import backend.mathsolver as msolver
import web

urls = (
	'/(.*)', 'main'
)

render = web.template.render('templates/')

class main():
	def GET(self, name):
		usr_data = web.input(q="")
		if usr_data.q == "":
			return render.start()
		else:
			solver = msolver.MathSolver()
			return render.results(usr_data.q,'$$' + solver.solve(str(usr_data.q)) + '$$')

app = web.application(urls, globals())

if __name__ == '__main__':
	app.run()