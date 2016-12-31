# Build a Gradle Project from Python

import os
import argparse
import shutil
import sys

class ChangeDirectory:
  def __init__(self, path):
    self.newpath=os.path.expanduser(path)

  def __enter__(self):
    self.oldpath=os.getcwd()
    os.chdir(self.newpath)
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    os.chdir(self.oldpath)

def arg_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument("--d", help="project name", type=str)
  parser.add_argument("--p", help="path to project home", type=str)
  return parser.parse_args()

def make_root(root_name):
  path = os.path.abspath(os.path.join(".", root_name))
  if os.path.exists(path):
    return path
  os.mkdir(root_name)
  return path

def make_src(proj_path):
  os.makedirs(os.path.join(proj_path, "src", "main", "java"))
  os.makedirs(os.path.join(proj_path, "src", "test", "java"))

def add_gradle_files(proj_path, gsrc):
  gfiles = os.listdir(gsrc)
  for f in gfiles:
    path = os.path.join(gsrc,f)
    if os.path.isfile(path):
      shutil.copy(path, proj_path)
    else:
      shutil.copytree(path, os.path.join(proj_path, f))

if __name__ == "__main__":
  args = arg_parser()
  if os.path.exists(args.p):
    with ChangeDirectory(args.p) as p:
      proj_path = make_root(args.d)
      try:
        make_src(proj_path)
        add_gradle_files(proj_path, os.path.join(p.oldpath, "GradleProjFiles"))
      except Exception as e:
        print e
        print("Caught an exception. Project will not be built.")
        shutil.rmtree(proj_path)
        sys.exit(1)
  else:
    raise ValueError("Directory does not exist: {}.".format(args.p))
