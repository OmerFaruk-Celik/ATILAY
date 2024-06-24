import paramiko
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, Polygon, MultiPolygon
from matplotlib.lines import Line2D
import alphashape

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
    Q1_y = data["y"].quantile(0.25)
    Q3_y = data["y"].quantile(0.85)
    IQR_y = Q3_y - Q1_y
    alt_sinir_y = Q1_y - 1.5 * IQR_y
    ust_sinir_y = Q3_y + 1.5 * IQR_y
    
    # X ekseni için aykırı değer temizleme
    Q1_x = data["x"].quantile(0.25)
    Q3_x = data["x"].quantile(0.85)
    IQR_x = Q3_x - Q1_x
    alt_sinir_x = Q1_x - 1.5 * IQR_x
    ust_sinir_x = Q3_x + 1.5 * IQR_x
    
    # Her iki eksen için sınırları kontrol et ve filtrele
    data_temiz = data[(data["y"] >= alt_sinir_y) & (data["y"] <= ust_sinir_y) & 
                      (data["x"] >= alt_sinir_x) & (data["x"] <= ust_sinir_x)]
    return data_temiz

def create_geodataframe(data):
    """Geometrik noktalar oluşturup GeoDataFrame döndüren fonksiyon"""
    geometry = [Point(xy) for xy in zip(data["x"], data["y"])]
    gdf = gpd.GeoDataFrame(data, geometry=geometry)
    return gdf

def calculate_alpha_shape(gdf, alpha):
    """Alpha Shape hesaplama fonksiyonu"""
    points = gdf[['x', 'y']].values
    alpha_shape = alphashape.alphashape(points, alpha)
    return alpha_shape

def plot_data_with_alpha_shape(gdf, lidar_start_point, alpha_shape):
    """Veri setini ve LIDAR başlangıç noktasını haritada gösteren fonksiyon"""
    fig, ax = plt.subplots(figsize=(10, 6))
    gdf.plot(ax=ax, color='blue', markersize=10, label="Veriler")
    
    if isinstance(alpha_shape, Polygon):
        alpha_shape_gdf = gpd.GeoDataFrame(geometry=[alpha_shape])
        alpha_shape_gdf.plot(ax=ax, color='none', edgecolor='purple', linewidth=2, label="Alpha Shape")
    elif isinstance(alpha_shape, MultiPolygon):
        for geom in alpha_shape.geoms:
            alpha_shape_gdf = gpd.GeoDataFrame(geometry=[geom])
            alpha_shape_gdf.plot(ax=ax, color='none', edgecolor='purple', linewidth=2, label="Alpha Shape")

    # LIDAR başlangıç noktasını ve vektörünü çiz
    ax.scatter(*lidar_start_point, color='red', s=10, label="LIDAR Başlangıç")
    ax.add_line(Line2D([lidar_start_point[0], lidar_start_point[0] + 0.1], 
                       [lidar_start_point[1], lidar_start_point[1] + 0.1], 
                       color='red', linewidth=2))

    ax.set_title("İki Boyutlu Veri Dağılımı ve Alpha Shape")
    ax.set_xlabel("Enlem")
    ax.set_ylabel("Boylam")
    
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

# GeoDataFrame oluştur
gdf = create_geodataframe(data_temiz)

# Alpha Shape hesapla
alpha = 0.003 # Alfa parametresi, verilerinize göre ayarlayabilirsiniz
alpha_shape = calculate_alpha_shape(gdf, alpha)

# LIDAR başlangıç noktası (0, 0)
lidar_start_point = (0, 0)

# Haritayı çiz
plot_data_with_alpha_shape(gdf, lidar_start_point, alpha_shape)
