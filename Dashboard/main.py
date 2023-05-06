from subprocess import run

is_running = True

def main():
    while is_running:
        run(["node", "httpget.js"])
        run(["node", "httpget.js"])
        run(["python", "test_graph.py"])

main()
