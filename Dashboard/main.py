from subprocess import run
import sys

is_running = True

def main():
    while is_running:
        run(["node", "httpget.js"])
        run(["python", "test_graph.py"])
main()
