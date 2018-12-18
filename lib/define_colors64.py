def colors64():
    '''
    Finds 64 colors by choosing the middle values in 
    each of the 64 small cubes in the RGB color cube.
    The first color will be [32,32,32], the next [96,32,32] and so on.
    
    RGB colors are used to train our perceptrons, but only with 64 colors.
    The RGB colors from the RGB cube are made from the values 255x255x255.
    '''
    colors = []
    for b in range(4):
        for g in range(4):
            for r in range(4):
                _r = 32 + r * 64
                _g = 32 + g * 64
                _b = 32 + b * 64
                colors.append([_r, _g, _b])
    return colors

color_list = colors64()
