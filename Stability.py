import numpy as np
import matplotlib.pyplot as plt
import plotly


class Stability():
    def __init__(self):
        None
    def volume(self):
        vol = 0

        return vol

def parseGDF(file):

    try:
        with open(f'{file}', "r") as gdf_file:
            data = gdf_file.read()

    except FileNotFoundError:
        print(FileNotFoundError)

    data = data.split("\n")
    header = 4

    for id,line in enumerate(data):
        if id == 1 :
            aux = line.strip(' ').split(" ")
            ULEN = int(aux[0])
            GRAV = float(aux[1])

        elif id == 2:
            aux = line.replace('','').split(" ")
            ISX = int(aux[0])
            ISY = int(aux[2])

        elif id == 3:
            n_patch = len(data)-header

            # Pre allocate vector for speed
            x = np.array([])
            y = np.array([])
            z = np.array([])

        elif id > 3:
            aux = line.strip(' ').split(" ")
            if len(aux) == 3:
                if ISY == 1 and ISX == 0 and float(aux[1])>=0:
                    # print("in 1")
                    x =   np.hstack((x, float(aux[0])))
                    y =   np.hstack((y, float(aux[1])))
                    z =   np.hstack((z, float(aux[2])))

                elif ISY == 0 and ISX == 1 and float(aux[0])>=0:
                    x = np.hstack((x, float(aux[0])))
                    y = np.hstack((y, float(aux[1])))
                    z = np.hstack((z, float(aux[2])))
                elif ISY == 1 and ISX == 1 and float(aux[0]) >= 0 and float(aux[1]) >= 0:
                    x = np.hstack((x, float(aux[0])))
                    y = np.hstack((y, float(aux[1])))
                    z = np.hstack((z, float(aux[2])))
                elif ISY == 0 and ISX == 0:
                    x = np.hstack((x, float(aux[0])))
                    y = np.hstack((y, float(aux[1])))
                    z = np.hstack((z, float(aux[2])))



    x = np.reshape(x, (len(x), 1))
    y = np.reshape(y, (len(x), 1))
    z = np.reshape(z, (len(x), 1))

    point_cloud = np.hstack((x,y,z))
    return point_cloud



def plot_object(point_cloud):

    max_x, min_x = max(point_cloud[:,0]), min(point_cloud[:,0])
    max_y, min_y = max(point_cloud[:, 1]), min(point_cloud[:, 1])
    max_z, min_z = max(point_cloud[:, 2]), min(point_cloud[:, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(pt[:, 0], pt[:, 1], pt[:, 2])

    hull_length = np.abs(max_x - min_x)
    hull_beam = np.abs(max_y - min_y)


    plt.xlim(-1*hull_length, 1*hull_length)
    plt.ylim(-2*hull_beam, 2*hull_beam)

    plt.show()

    return

def norm(vector):
    return np.sqrt(np.sum(np.power(vector,2)))

def normal_vec(vertices):
    vertex_1 = vertices[0]
    vertex_2 = vertices[1]
    vertex_3 = vertices[2]

    vec_1 = vertex_2 - vertex_1
    vec_2 = vertex_3 - vertex_1

    normal_unit = np.cross(vec_1,vec_2)/np.dot(vec_1,vec_2)

    return normal_unit


def volume(point_cloud, wl):
    '''Calculate underwater volume'''
    underwater_vol = 0

    for id, panel in enumerate(point_cloud):
        if id%3 == 0:
            normal_vec([point_cloud[id], point_cloud[id+1], point_cloud[id+2]])


    return underwater_vol



def surface_area(point_cloud):
    area = 0
    point_cloud = sort_pt(point_cloud, axis=1)
    for id, panel in enumerate(point_cloud):
        if id%3 == 0 and  id < len(point_cloud)-3:
            if id == len(point_cloud) - 2:
                vec_2 = point_cloud[-1]-point_cloud[id]
                vec_1 = point_cloud[id + 1] - point_cloud[id]
            elif id == len(point_cloud) - 1:
                vec_2 = point_cloud[-2] - point_cloud[id]
                vec_1 = point_cloud[-1] - point_cloud[id]
            else:
                vec_2 = point_cloud[id + 2] - point_cloud[id]
                vec_1 = point_cloud[id + 1] - point_cloud[id]
            area += norm(np.cross(vec_1,vec_2))

    return area

def sort_pt(array,axis=None):
    mask = np.argsort(array, axis)
    sorted = np.zeros(array.shape)
    for id, val in enumerate(array):
        sorted[id,:] = array[mask[id][axis]]
    return sorted




def main():

    return

def create_shape(B, D, T):
    n = 20
    waterline = np.linspace(0, 0, n)

    top_x = np.linspace(-B / 2, B / 2, n)
    top_y = np.linspace(D - T, D - T, n)

    bottom_x = np.linspace(-B / 2, B / 2, n)
    bottom_y = np.linspace(-T, -T, n)

    portside_x = np.linspace(-B/2, -B/2, n)
    portside_y = np.linspace(-T, D-T, n)

    starboard_x = np.linspace(B/2, B/2, n)
    starboard_y = np.linspace(-T, D-T, n)

    x = np.hstack((top_x, starboard_x, bottom_x, portside_x))
    y = np.hstack((top_y, starboard_y, bottom_y, portside_y))


    return [x,y]

def plot_figure(shape):
    xmax = np.max(shape[0])
    ymax = np.max(shape[1])
    scale = 1.5
    waterline_x = np.linspace(-scale*xmax,scale*xmax,10)
    waterline_y = np.linspace(-1.5*0,1.5*0,10)
    fig = plt.figure()
    for i,point in enumerate(shape[1]):
        r = np.sqrt(shape[0][i] ** 2 + shape[1][i] ** 2)

        print(f'{r,shape[0][i],shape[1][i]=}')

        if r == np.sqrt(2):
            print("in")
            plt.scatter(shape[0][i], shape[1][i], c="r")

        elif point<=0:
            plt.scatter(shape[0][i],shape[1][i],c="g")
        else:
            plt.scatter(shape[0][i], shape[1][i], c="b")
    plt.plot(waterline_x,waterline_y)
    plt.xlim(-scale*xmax, scale*xmax)
    plt.ylim(-scale*ymax, scale*ymax)
    plt.grid()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
    return

def rotate(shape,center,angle):

    for i, point in enumerate(shape[0]):
        print(f'{shape[0][i],shape[1][i]}\n')

        r = np.sqrt(shape[0][i]**2+shape[1][i]**2)
        theta = angle*np.pi/180
        shape[0][i] = shape[0][i]*np.cos(theta)-shape[1][i]*np.sin(theta)
        shape[1][i] = shape[0][i]*np.sin(theta)+shape[1][i]*np.cos(theta)**2


    return shape


if __name__ == "__main__":
    # main()
    # shape = create_shape(B=2,D=2,T=1)
    # plot_figure(shape)
    # plot_figure(rotate(shape,[0,0],45))

    path = "C:\\Users\\rauad\\PycharmProjects\\pythonProject\\VPP\\Input\\Hulls"
    file = "barehull.gdf"
    pt = parseGDF(f"{path}\\{file}")
    # pt = np.array([[-1,2,5],[3,5,2],[-3,2,-33],[0,2,21],[23,-32,0]])
    # plot_object(pt)
    print(f"surface Area = {surface_area(pt)}")
    # print(pt)
    # print(f"Sorted pt = {sort_pt(pt,axis = 0)}")

    # Area = 2247.3671 (+/- 0.00063) square meters
    # Volume = 4794.36864 (+/- 1e-06) cubic meters
    # @ WL = 0.0:
    # Volume Displacement = 1693.8
    # Center of Buoyancy = 18.8005, 6.39935e-16, -1.64352
    # Wetted Surface Area = 790.033
    # Waterline Length = 55.7235
    # Maximum Waterline Beam = 14.6151
    # Water Plane Area = 642.858
    # Center of Floatation = 18.2215, -3.32771e-15,0
    #
    # @ WL = 1.0 m
    # Volume Displacement = 2376.01
    # Center of Buoyancy = 18.6221, -3.75904e-15, -1.02549
    # Wetted Surface Area = 939.837
    # Waterline Length = 58.5033
    # Maximum Waterline Beam = 15.2518
    # Water Plane Area = 716.532
    # Center of Floatation = 18.2366, -8.83684e-15,1

    # Do objeto completo :
    # Area = 2247.3671 (+/- 0.00063) square meters
    # Area Centroid = 19.774333,-1.01173357e-15,1.275459 (+/- 1.3e-05,4.2e-08,1.4e-06)
    # Area Moments:
    #    First Moments
    #    x: 	44440.186 (+/- 0.016)
    #    y: 	-2.2737368e-12 (+/- 9.4e-05)
    #    z: 	2866.4251 (+/- 0.0023)
    #    Second Moments
    #    xx: 	1507160 (+/- 1.8)
    #    yy: 	49048.019 (+/- 0.0091)
    #    zz: 	24420.716 (+/- 0.012)
    #    Product Moments
    #    xy: 	-4.20910359e-11 (+/- 0.0019)
    #    yz: 	-1.01760162e-11 (+/- 0.0015)
    #    zx: 	72141.83 (+/- 0.12)
    #    Area Moments of Inertia about World Coordinate Axes
    #    Ix: 	73468.735 (+/- 0.021)
    #    Iy: 	1531581 (+/- 1.8)
    #    Iz: 	1556208 (+/- 1.8)
    #    Area Radii of Gyration about World Coordinate Axes
    #    Rx: 	5.7176066 (+/- 1.6e-06)
    #    Ry: 	26.105557 (+/- 1.9e-05)
    #    Rz: 	26.314605 (+/- 1.9e-05)
    #    Area Moments of Inertia about Centroid Coordinate Axes
    #    Ix: 	69812.727 (+/- 0.012)
    #    Iy: 	649149.89 (+/- 0.38)
    #    Iz: 	677433.2 (+/- 0.39)
    #    Area Principal Moments of Inertia about Centroid and Principal Axes
    #    I1: 	69419.615 , 	 Direction ( 0.99967688, 0 ,0.025419147)
    #    I2: 	649149.89 , 	 Direction ( 0, 1 ,0)
    #    I3: 	677826.32 , 	 Direction ( -0.025419147, 0 ,0.99967688)
    #    Area Radii of Gyration about Centroid Coordinate Axes
    #    Rx: 	5.5735293 (+/- 1.3e-06)
    #    Ry: 	16.99556 (+/- 7.3e-06)
    #    Rz: 	17.361859 (+/- 7.4e-06)


    # Volume = 4800.98273 (+/- 1e-06) cubic meters
    # Volume Centroid = 20.0457297,-9.47196389e-16,0.822832664 (+/- 1.5e-08,9.7e-15,1e-10)
    # Volume Moments:
    #    First Moments
    #    x: 	96239.2021 (+/- 7.1e-05)
    #    y: 	-4.54747351e-12 (+/- 4.6e-11)
    #    z: 	3950.40541 (+/- 1e-06)
    #    Second Moments
    #    xx: 	2948323.82 (+/- 0.12)
    #    yy: 	64440.7765 (+/- 0.00055)
    #    zz: 	26090.8876 (+/- 0.00075)
    #    Product Moments
    #    xy: 	-1.40724886e-10 (+/- 2e-06)
    #    yz: 	5e-12 (+/- 0.00012)
    #    zx: 	102233.201 (+/- 0.0078)
    #    Volume Moments of Inertia about World Coordinate Axes
    #    Ix: 	90531.6641 (+/- 0.0013)
    #    Iy: 	2974414.71 (+/- 0.12)
    #    Iz: 	3012764.6 (+/- 0.12)
    #    Volume Radii of Gyration about World Coordinate Axes
    #    Rx: 	4.34245353 (+/- 3.1e-08)
    #    Ry: 	24.8906185 (+/- 5e-07)
    #    Rz: 	25.0505651 (+/- 5e-07)
    #    Volume Moments of Inertia about Centroid Coordinate Axes
    #    Ix: 	87281.1415 (+/- 0.0013)
    #    Iy: 	1041979.2 (+/- 0.12)
    #    Iz: 	1083579.6 (+/- 0.12)
    #    Volume Principal Moments of Inertia about Centroid and Principal Axes
    #    I1: 	86748.407 , 	 Direction ( 0.999732893, 0 ,0.0231115238)
    #    I2: 	1041979.15 , 	 Direction ( 0, 1 ,0)
    #    I3: 	1084112.3 , 	 Direction ( -0.0231115238, 0 ,0.999732893)
    #    Volume Radii of Gyration about Centroid Coordinate Axes
    #    Rx: 	4.26378342 (+/- 3.2e-08)
    #    Ry: 	14.7320927 (+/- 8.3e-07)
    #    Rz: 	15.0232997 (+/- 8.1e-07)






    # Descrição do procedimento de determinação da curva de estabilidade da embarcação
    # 1 -  INPUTS
    #       1.1 Barco GDF
    #       1.2 Calado inicial
    #       1.3 Centro de Gravidade
    #       1.4 Presença e posição de eventuais tanques de líquidos (Sup. Livre)
    #       1.5 Posição de entradas de água? non-watertight spaces
    # 2 - CALCULO
    #       2.0 Tratar os dados do arquivo GDF
    #       2.1 Encontrar a matriz de estabilidade dada em Neumann (ou WAMIT)
    #       2.2 Dar um angulo de banda inicial
    #           2.2.1 Calcular o novo volume deslocado
    #           2.2.2 Se o novo vol Deslocado =! antigo vol deslocado subir ou descer a embarcação
    #               2.1.2.1 Recalcular o vol deslocado
    #           2.2.3 Recalcular a posiçao do centro de carena
    #           2.2.4 Indicar valores de forças e momentos e salvar em um vetor
    #           2.2.5 Indicar a posição do metacentro e guardar o seu valor
    #           2.2.6 Fatiar o volume submerso e retirar a área de cada fatia transversal
    #           2.2.7 Encontrar os parametros da embarcaçao adernada
    #               2.2.7.1 Encontrar o calado na posição adernada
    #               2.2.7.2 Comprimento de linha dágua
    #               2.2.7.3 Coeficientes (Cb, Cp, Cawp etc.)