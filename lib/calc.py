def tensaoNormal(Fzsd, Aew, Iy, Ix, Ixy, Mxsd, Mysd, x, y):
    a = Fzsd / Aew
    b = (Mxsd * Iy + Mysd * Ixy) * y
    c = (Mysd * Ix + Mxsd * Ixy) * x
    d = Ix * Iy - Ixy ** 2
    SIGwsd = a + ((b - c) / d)

    return SIGwsd


def calculoCisalhamento(Fxsd, Fysd, Aew, Mzsd, x, y, Ix, Iy):
    Iz = Ix + Iy
    TAUwxsd = (Fxsd / Aew) - ((Mzsd * y) / Iz)
    TAUwysd = (Fysd / Aew) + ((Mzsd * x) / Iz)
    TAUwsd = (TAUwysd ** 2 + TAUwxsd ** 2) ** (1 / 2)

    return TAUwxsd, TAUwysd, TAUwsd

def momentoInerciaSolda(tw, xi, yi, xf, yf):
    import numpy as np
    # Calcula o comprimento de cada solda e a variação em x e y
    dx = np.array(xf) - np.array(xi)
    dy = np.array(yf) - np.array(yi)
    comprimentos = np.sqrt(dx ** 2 + dy ** 2)

    # Calcula a área de cada solda (comprimento x espessura)
    areas = np.array(tw) * comprimentos

    # Calcula as coordenadas centrais de cada solda
    x_centrais = (np.array(xi) + np.array(xf)) / 2
    y_centrais = (np.array(yi) + np.array(yf)) / 2

    # Calcula inércia e produto de inércia
    inercia_x = np.sum((comprimentos * tw * (dy ** 2 + 3 * dy * yi + 3 * yi ** 2))/3)
    inercia_y = np.sum((comprimentos * tw * (dx ** 2 + 3 * dx * xi + 3 * xi ** 2))/3)
    inercia_xy = np.sum((comprimentos * tw * (2 * dx * dy + 3 * dy * xi + 3 * dx * yi + 6 * xi * yi)) / 6)

    return inercia_x, inercia_y, inercia_xy
def momentoInerciaParafuso(diametro, coord_x, coord_y):
    import numpy as np

    area = [0] * len(diametro)
    inercia_y = 0
    inercia_x = 0
    inercia_xy = 0
    j = 0

    for k in range(0, len(diametro)):
        area[k] = np.pi * (diametro[k] ** 2) / 4

    for k in range(0, len(area)):
        j = (coord_x[k] ** 2) * area[k]
        inercia_y = inercia_y + j

    for k in range(0, len(area)):
        j = (coord_y[k] ** 2) * area[k]
        inercia_x = inercia_x + j

    for k in range(0, len(area)):
        j = coord_y[k] * coord_x[k] * area[k]
        inercia_xy = inercia_xy + j



    return inercia_x, inercia_y, inercia_xy


def determinaPropriedadesLigacao(d, x,  y, tw, xi, yi, xf, yf):
    """
    Essa função determina os parametros da ligação como um todo

    """

    import numpy as np
    # Parafusos
    if len(d) == 0:
        total_area_b = 0.
        cgx_b = 0.
        cgy_b = 0.
    else:
        area_b = np.pi * (np.array(d) ** 2) / 4
        total_area_b = np.sum(area_b)
        cgx_b = np.sum(x * area_b) / total_area_b
        cgy_b = np.sum(y * area_b) / total_area_b

    # Soldas
    if len(tw) == 0:
        total_area_s = 0.
        cgx_s = 0.
        cgy_s = 0.
    else:
        # Calcula o comprimento de cada solda
        comprimentos = np.sqrt((np.array(xf) - np.array(xi))**2 + (np.array(yf) - np.array(yi))**2)

        # Calcula a área de cada solda (comprimento x espessura)
        areas_s = np.array(tw) * comprimentos

        # Calcula as coordenadas centrais de cada solda
        x_centrais = (np.array(xi) + np.array(xf)) / 2
        y_centrais = (np.array(yi) + np.array(yf)) / 2

        # Calcula o centróide ponderado pela área
        total_area_s = np.sum(areas_s)
        cgx_s = np.sum(x_centrais * areas_s) / total_area_s
        cgy_s = np.sum(y_centrais * areas_s) / total_area_s

    cgx = (cgx_b * total_area_b + cgx_s * total_area_s)/(total_area_b + total_area_s)
    cgy = (cgy_b * total_area_b + cgy_s * total_area_s)/(total_area_b + total_area_s)

    # Altera as coordenadas dos parafusos e das soldas para coincidirem com o CG
    # Daqui para frente todas as coordenadas são em relação ao centróide da ligação
    x = x - cgx
    y = y - cgy
    xi = xi - cgx
    yi = yi - cgy
    xf = xf - cgx
    yf = yf - cgy

    # Cálcula as propriedades das ligações individuais em relação ao centróide da ligação total
    # Parafusos
    Ibx, Iby, Ibxy = momentoInerciaParafuso(d, x, y)
    # Soldas
    Isx, Isy, Isxy = momentoInerciaSolda(tw, xi, yi, xf, yf)

    # Uni as propriedades da solda e dos parafusos
    # As propriedades só podem ser somadas desta forma caso elas forem calculadas em relação ao mesmo centróide
    Ix = Ibx + Isx  # inercia em relação a x da ligação
    Iy = Iby + Isy  # inercia em relação a y da ligação
    Ixy = Ibxy + Isxy  # produto de inercia da ligação
    At = total_area_b + total_area_s  # Área da ligação

    return At, cgx, cgy, Ix, Iy, Ixy
