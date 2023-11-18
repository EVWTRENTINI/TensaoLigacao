import numpy as np
from mpl_toolkits.mplot3d import art3d
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d.proj3d import proj_transform
from mpl_toolkits.mplot3d.axes3d import Axes3D


def drawParafuso(x, y, d, ax):

    h = d * .2
    lados=6
    def detXY(x,y,d):
        r = d / 2

        passo = 2 * np.pi / (lados)
        th = np.arange(0, 2 * np.pi, passo)
        X = r * np.cos(th) + x
        Y = r * np.sin(th) + y
        return X,Y

    def drawTampa(x,y,z,d,lados, ax):
        X,Y=detXY(x,y,d)
        Z = np.full(lados, z)

        v = np.zeros(shape=(lados + 1, 3))
        for i in range(0, lados):
            v[i] = np.array([Z[i], X[i], Y[i]])
        v[lados] = np.array([z,x,y])

        f = np.zeros(shape=(lados, 3), dtype=int)
        for i in range(0, lados):
            f[i] = np.array([i, i+1, lados])
        f[lados-1][2] = 0

        pc = art3d.Poly3DCollection(v[f], facecolor="grey",zorder=-1000)
        ax.add_collection3d(pc)

        return ax

    def drawLateralCabeca(x,y,h,d,lados,ax):
        X, Y = detXY(x, y, d)

        #laterais menos 1
        for j in range(lados-1):
            v = np.zeros(shape=(4, 3))
            v[0] = np.array([0,X[j],Y[j]])
            v[1] = np.array([0,X[j+1],Y[j+1]])
            v[2] = np.array([h,X[j+1],Y[j+1]])
            v[3] = np.array([h,X[j],Y[j]])


            f = np.zeros(shape=(2, 3), dtype=int)
            f[0] = np.array([0, 1, 3])
            f[1] = np.array([1, 2, 3])

            pc = art3d.Poly3DCollection(v[f], facecolor="grey")
            ax.add_collection3d(pc)

        # Ultima lateral
        v = np.zeros(shape=(4, 3))
        v[0] = np.array([0, X[lados - 1], Y[lados - 1]])
        v[1] = np.array([0, X[0], Y[0]])
        v[2] = np.array([h, X[0], Y[0]])
        v[3] = np.array([h, X[lados - 1], Y[lados - 1]])
        f = np.zeros(shape=(2, 3), dtype=int)
        f[0] = np.array([0, 1, 3])
        f[1] = np.array([1, 2, 3])

        pc = art3d.Poly3DCollection(v[f], facecolor="grey")
        ax.add_collection3d(pc)

        return ax


    ax=drawTampa(x,y,0,d,lados,ax)
    ax=drawTampa(x,y,h,d,lados,ax)

    ax = drawLateralCabeca(x, y, h, d, lados, ax)


    return ax

class Arrow3D(FancyArrowPatch):

    def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._xyz = (x, y, z)
        self._dxdydz = (dx, dy, dz)


    def draw(self, renderer):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        super().draw(renderer)


    def do_3d_projection(self, renderer=None):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))

        return np.min(zs)

def _arrow3D(ax, x, y, z, dx, dy, dz, *args, **kwargs):
    arrow = Arrow3D(x, y, z, dx, dy, dz, *args, **kwargs)
    ax.add_artist(arrow)
setattr(Axes3D, 'arrow3D', _arrow3D)

