__author__ = 'markus'

from pybuilder.core import init, use_plugin

use_plugin("python.core")
use_plugin("python.install_dependencies")

default_task = ['install_dependencies', 'publish']

@init
def initialize(project):
  project.set_property('dir_source_main_python', '/drei')
  project.set_property('dir_install_logs', 'logs')
  init_dependencies(project)

def init_dependencies(project):
    project.build_depends_on('numpy', version="1.8.2")
    project.build_depends_on('itertools-recipes')
    project.build_depends_on('Flask', version="0.10.1")
    project.build_depends_on('Flask-Cors', version="2.0.0")
    project.build_depends_on('Flask-RESTful', version="0.3.2")
    project.build_depends_on('Flask-SocketIO', version="0.6.0")
    project.build_depends_on('pyserial')
#    project.build_depends_on('pygame', version="1.9.1release")
