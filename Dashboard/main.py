import test_graph.py
import httpget.js
from subprocess import call
import subprocess

is_running = true


def main () :
  while is_running:
      call(["node","httpget.js"])
      call(["python","test_graph.py"])

main()