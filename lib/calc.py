def tensaoNormal(Fzsd, Aew, Iy, Ix, Ixy, Mxsd, Mysd, x, y):
    a = Fzsd / Aew
    b = (Mxsd * Iy + Mysd * Ixy) * y
    c = (Mysd * Ix + Mxsd * Ixy) * x
    d = Ix * Iy - Ixy ** 2
    # todo(Eduardo) Fazer verificação a baixo
    print('Fazer a verificação se (Ix * Iy - Ixy ** 2) = 0')
    SIGwsd = a + ((b - c) / d)

    return SIGwsd


def calculoCisalhamento(Fxsd, Fysd, Aew, Mzsd, x, y, Ix, Iy):
    Iz = Ix + Iy
    TAUwxsd = (Fxsd / Aew) - ((Mzsd * y) / Iz)
    TAUwysd = (Fysd / Aew) + ((Mzsd * x) / Iz)
    TAUwsd = (TAUwysd ** 2 + TAUwxsd ** 2) ** (1 / 2)

    return TAUwxsd, TAUwysd, TAUwsd


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

    areaTotal = sum(area)

    return inercia_x, inercia_y, inercia_xy, areaTotal


def determinaPropriedadesLigacao(diametro_parafuso, coord_x_parafuso,
                                 coord_y_parafuso):  # todo(Eduardo):  Incluir listas das soldas
    """
    Essa função determina os parametros da ligação como um todo

    """

    import numpy as np
    # Parafusos
    area_parafusos = np.pi * (np.array(diametro_parafuso) ** 2) / 4
    total_area_b = np.sum(area_parafusos)
    cgx_b = np.sum(coord_x_parafuso * area_parafusos) / total_area_b
    cgy_b = np.sum(coord_y_parafuso * area_parafusos) / total_area_b

    # Soldas
    # Todo(Eduardo): Calcular o centróide da ligação incluindo soldas
    # Todo(Eduardo): Calcular o centróide, apagar este bloco                ####### INICIO #############
    print('Desenvolver função que determina o centróide da ligação considerando soldas')  ####
    cgx = cgx_b  # Coordenada x do centróide da ligação                                                 ####
    cgy = cgy_b  # Coordenada y do centróide da ligação                                                 ####
    # Todo(Eduardo): Calcular o centróide, apagar este bloco               ########  FIM  #############

    # Altera as coordenadas para dos parafusos e das soldas para coincidirem com o CG
    # Daqui para frente todas as coordenadas são em relação ao centróide da ligação
    coord_x_parafuso = coord_x_parafuso - cgx
    coord_y_parafuso = coord_y_parafuso - cgy
    # Todo(Eduardo): Alterar as coordenadas das soldas dentro deste escopo

    # Cálcula as propriedades das ligações individuais em relação ao centróide da ligação total
    # Parafusos
    Ibx, Iby, Ibxy, Atb = momentoInerciaParafuso(diametro_parafuso, coord_x_parafuso, coord_y_parafuso)
    # Soldas
    # Todo(Eduardo): fazer função que calcula área total e inércia das soldas. Chamar ela aqui
    '''#######
    ##########
    FAZER AQUI
    ##########
    #######'''

    # Todo(Eduardo): Após fazer e chamar a função acima, apagar este bloco ####### INICIO #############
    print('Desenvolver função que determina as propriedades das soldas. Utilizando zero até entao.')  ####
    Isx = 0  # inercia em relação a x das soldas                                                    ####
    Isy = 0  # inercia em relação a y das soldas                                                    ####
    Isxy = 0  # produto de inercia das soldas                                                       ####
    Ats = 0  # Área das soldas                                                                     ####
    # Todo(Eduardo): Após fazer e chamar a função acima, apagar este bloco #####  FIM  ###############

    # Uni as propriedades da solda e dos parafusos
    # As propriedades só podem ser somadas desta forma caso elas forem calculadas em relação ao mesmo centróide
    Ix = Ibx + Isx  # inercia em relação a x da ligação
    Iy = Iby + Isy  # inercia em relação a y da ligação
    Ixy = Ibxy + Isxy  # produto de inercia da ligação
    At = Atb + Ats  # Área da ligação

    return At, cgx, cgy, Ix, Iy, Ixy
