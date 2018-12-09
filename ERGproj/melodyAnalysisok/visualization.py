import pandas as pd
import numpy as np
import math
from sklearn.decomposition import PCA
from pyecharts import Scatter3D
from scipy.spatial import Voronoi, voronoi_plot_2d

def _3dAnalysis():
    csvFile = pd.read_csv("songdata.csv", sep = ",")

    # Extract feature matrix (i.e. remove the first three columns)
    feature = csvFile.ix[:,2:]

    pca = PCA(n_components=3)
    pca.fit(feature)

    feature_new = pca.fit_transform(feature)
    feature_new[:,0] = [feature_new[i][0]/1e8 for i in range(len(feature_new))]
    feature_new[:,1] = [feature_new[i][1]/1e7 for i in range(len(feature_new))]
    feature_new[:,2] = [feature_new[i][2]/1e6 for i in range(len(feature_new))]

    mark_list = []
    name = list(csvFile.ix[:,1])
    for i in range(len(feature_new)):
        mark_list.append({"coord": list(feature_new[i]), "name": name[i]})
    # visualization
    range_color = [
            '#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
            '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
    scatter3D = Scatter3D("Music Classification", width=800, height=600, title_pos = 'center')
    scatter3D.add("", feature_new, mark_point = mark_list, is_visualmap=True, visual_range_color=range_color, grid3d_opacity = 3,
                  visual_pos = 'left',xaxis3d_name = "PCA1", yaxis3d_name = "PCA2",zaxis3d_name = "PCA3",is_grid3d_rotate = True)
    scatter3D.render("3Dscatter.html")

_3dAnalysis()