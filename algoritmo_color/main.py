from Color_map import Color_map

if __name__ == "__main__":
    cp = Color_map()
    print(cp.gen_random_individuo().shape)
    cp.evolucionar()
    