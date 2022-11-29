import os
import shutil

import nox

ON_GITHUB = 'GITHUB_ACTIONS' in os.environ

py39 = '3.9'
py310 = '3.10'


nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = [
	'lint',
	'doc',
	'test'
]


@nox.session
def lint(session):
	session.install('-U', '.[lint]')
	session.run('flake8', 'src/', 'tests/')


@nox.session
def doc(session):
	shutil.rmtree('docs/_build', ignore_errors=True)
	session.install('-U', '.[doc]')
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


@nox.session(python=[py39, py310])
def test(session):
	session.install('-U', '.[test]')
	session.run('coverage', 'run', '-m', 'ward', *session.posargs)
	session.notify('report')


@nox.session(python=[py39, py310])
def integration(session):
	session.install('-U', '.[test]')
	session.run('coverage', 'run', '-m', 'ward', '--tags', 'integration', *session.posargs)
	session.notify('report')


@nox.session(python=[py39, py310])
def unit(session):
	session.install('-U', '.[test]')
	session.run('coverage', 'run', '-m', 'ward', '--tags', 'unit', *session.posargs)
	session.notify('report')


@nox.session
def report(session):
	session.install('-U', 'coverage[toml]')

	if ON_GITHUB:
		session.run('coverage', 'xml')
	else:
		session.run('coverage', 'report', '-m')
		session.run('coverage', 'erase')
