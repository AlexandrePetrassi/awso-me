from src.Initialization import Awsome
from src.ArgumentParsing import ProgramArguments

if __name__ == '__main__':
    shared_pids: list = []
    app, args, fu_tps, grid, finder = ProgramArguments.parse_args()
    Awsome.start(app, args, shared_pids, fu_tps, grid, finder)
