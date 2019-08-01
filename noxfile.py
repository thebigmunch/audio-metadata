import nox

py36 = '3.6'
py37 = '3.7'
py38 = '3.8'


@nox.session(python=py37)
def lint(session):
	session.install('.[lint]')
	session.run('flake8', 'src/', 'tests/')


@nox.session(python=py37)
def doc(session):
	session.run('rm', '-rf', 'docs/_build', external=True)
	session.install('.[doc]')
	session.cd('docs')
	session.run(
		'sphinx-build',
		'-b',
		'html',
		'-W',
		'-d',
		'_build/doctrees',
		'.',
		'_build/html'
	)


@nox.session(python=[py36, py37, py38])
def test(session):
	session.install('.[test]')
	session.run('coverage', 'run', '--parallel', '-m', 'pytest')


@nox.session(python=py37)
def coverage(session):
	session.install('coverage')
	session.run('coverage', 'combine')
	session.run('coverage', 'report', '-m')
