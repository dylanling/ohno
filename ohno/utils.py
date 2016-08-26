def grid_from_file(filename):
    grid = []
    with open(filename) as f:
        for line in f.readlines():
            grid.append(map(lambda x: int(x) if x.isdigit() else x, line.rstrip()))
    return grid