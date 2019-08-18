import os
import shutil

import nox

py36 = '3.6'
py37 = '3.7'
py38 = '3.8'

ON_TRAVIS = 'TRAVIS' in os.environ


@nox.session(python=py37)
def lint(session):
	session.install('.[lint]')
	session.run('flake8', 'src/', 'tests/')


@nox.session(python=py37)
def doc(session):
	shutil.rmtree('docs/_build', ignore_errors=True)
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
	session.notify('coverage')
	session.notify('report')


@nox.session
def coverage(session):
	session.install('.[test]')
	session.run('coverage', 'run', '-m', 'pytest')
	session.notify('report')


@nox.session
def report(session):
	session.install('coverage')
	session.run('coverage', 'report', '-m')

	if ON_TRAVIS:
		session.install('codecov')
		session.run('codecov')

	session.run('coverage', 'erase')
