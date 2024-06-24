import paramiko
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
from matplotlib.lines import Line2D
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA

def ssh_download_file(hostname, username, password, remote_path, local_path):
    """SSH üzerinden dosya indirme fonksiyonu"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, username=username, password=password)
    with client.open_sftp() as sftp:
        sftp.get(remote_path, local_path)
    client.close()

def read_and_clean_data(file_path):
    """CSV dosyasını okuyup aykırı değerleri temizleme fonksiyonu"""
    data = pd.read_csv(file_path)
    
    # Y ekseni için aykırı değer temizleme
    Q1_y = data["y"].quantile(0.15)
    Q3_y = data["y"].quantile(0.85)
    IQR_y = Q3_y - Q1_y
    alt_sinir_y = Q1_y - 1.5 * IQR_y
    ust_sinir_y = Q3_y + 1.5 * IQR_y
    
    # X ekseni için aykırı değer temizleme
    Q1_x = data["x"].quantile(0.15)
    Q3_x = data["x"].quantile(0.85)
    IQR_x = Q3_x - Q1_x
    alt_sinir_x = Q1_x - 1.5 * IQR_x
    ust_sinir_x = Q3_x + 1.5 * IQR_x
    
    # Her iki eksen için sınırları kontrol et ve filtrele
    data_temiz = data[(data["y"] >= alt_sinir_y) & (data["y"] <= ust_sinir_y) & 
                      (data["x"] >= alt_sinir_x) & (data["x"] <= ust_sinir_x)]
    return data_temiz

def rotate_data(data):
    """Verileri PCA kullanarak döndürme fonksiyonu"""
    pca = PCA(n_components=2)
    rotated_data = pca.fit_transform(data[['x', 'y']])
    data['x_rotated'] = rotated_data[:, 0]
    data['y_rotated'] = rotated_data[:, 1]
    return data

def create_geodataframe(data, x_col='x_rotated', y_col='y_rotated'):
    """Geometrik noktalar oluşturup GeoDataFrame döndüren fonksiyon"""
    geometry = [Point(xy) for xy in zip(data[x_col], data[y_col])]
    gdf = gpd.GeoDataFrame(data, geometry=geometry)
    return gdf

def plot_data(gdf, lidar_start_point):
    """Veri setini ve LIDAR başlangıç noktasını haritada gösteren fonksiyon"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Yoğunluk tabanlı kümeleme kullanarak yoğun bölgeleri belirle
    clustering = DBSCAN(eps=20, min_samples=5).fit(gdf[['x_rotated', 'y_rotated']])
    gdf['cluster'] = clustering.labels_
    
    # Yoğun bölgeler dışındaki noktaları belirle
    outside_bounds = gdf[gdf['cluster'] == -1]
    inside_bounds = gdf[gdf['cluster'] != -1]
    
    # Verileri çizme
    inside_bounds.plot(ax=ax, color='purple', markersize=10, label="Kenarlık İçindeki Veriler")
    outside_bounds.plot(ax=ax, color='blue', markersize=10, label="Veriler")
    
    # LIDAR başlangıç noktasını ve vektörünü çiz
    ax.scatter(*lidar_start_point, color='red', s=100, label="LIDAR Başlangıç")
    ax.add_line(Line2D([lidar_start_point[0], lidar_start_point[0] + 0.1], 
                       [lidar_start_point[1], lidar_start_point[1] + 0.1], 
                       color='red', linewidth=2))

    ax.set_title("İki Boyutlu Veri Dağılımı")
    ax.set_xlabel("Enlem")
    ax.set_ylabel("Boylam")
    #ax.legend()
    # Legende dışarı taşma sorunu çözümü
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.) 
    plt.show()

# SSH bilgileri
hostname = '192.168.7.11'
username = 'rasp'
password = '123'
remote_path = '/home/rasp/atilay/veriler.csv'
local_path = 'veriler.csv'

# Dosya indirme
ssh_download_file(hostname, username, password, remote_path, local_path)

# Veriyi oku ve temizle
data_temiz = read_and_clean_data(local_path)

# Veriyi döndür
data_rotated = rotate_data(data_temiz)

# GeoDataFrame oluştur
gdf = create_geodataframe(data_rotated, x_col='x_rotated', y_col='y_rotated')

# LIDAR başlangıç noktası (0, 0)
lidar_start_point = (0, 0)

# Haritayı çiz
plot_data(gdf, lidar_start_point)
