import paramiko
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.ops import nearest_points
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
    Q1_y = data["y"].quantile(0.15)
    Q3_y = data["y"].quantile(0.75)
    IQR_y = Q3_y - Q1_y
    alt_sinir_y = Q1_y - 1.5 * IQR_y
    ust_sinir_y = Q3_y + 1.5 * IQR_y
    
    # X ekseni için aykırı değer temizleme
    Q1_x = data["x"].quantile(0.15)
    Q3_x = data["x"].quantile(0.75)
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

def nokta_ici_mi(nokta, alpha_shape):
    """Noktanın alpha shape içinde olup olmadığını kontrol eden fonksiyon"""
    return alpha_shape.contains(Point(nokta))

def nokta_cizgiye_yakin_mi(nokta, alpha_shape, mesafe):
    """Noktanın alpha shape çizgisine belirli bir mesafeden daha yakın olup olmadığını kontrol eden fonksiyon"""
    point = Point(nokta)
    nearest_geom = nearest_points(point, alpha_shape.boundary)[1]
    return point.distance(nearest_geom) <= mesafe

def plot_data_with_alpha_shape(gdf, lidar_start_point, lidar_vector, alpha_shape, cizgi_mesafe):
    """Veri setini ve LIDAR başlangıç noktasını haritada gösteren fonksiyon"""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Alpha shape koordinatlarını elde etme
    if isinstance(alpha_shape, Polygon):
        x_coords, y_coords = alpha_shape.exterior.xy
        x_list = list(x_coords)
        y_list = list(y_coords)

    # Tüm noktaları alpha shape koordinatları ile karşılaştırarak renklendirme
    gdf['color'] = gdf.apply(lambda row: 'blue' if nokta_cizgiye_yakin_mi((row.x, row.y), alpha_shape, cizgi_mesafe) else ('purple' if nokta_ici_mi((row.x, row.y), alpha_shape) else 'blue'), axis=1)
    
    # Noktaları çiz
    for color, group in gdf.groupby('color'):
        group.plot(ax=ax, color=color, markersize=10, label=f"Veriler ({color})")

    # Alpha shape sınırlarını çiz
    if isinstance(alpha_shape, Polygon):
        alpha_shape_gdf = gpd.GeoDataFrame(geometry=[alpha_shape])
        alpha_shape_gdf.plot(ax=ax, color='none', edgecolor='blue', linewidth=2, label="Alpha Shape")
    elif isinstance(alpha_shape, MultiPolygon):
        for geom in alpha_shape.geoms:
            alpha_shape_gdf = gpd.GeoDataFrame(geometry=[geom])
            alpha_shape_gdf.plot(ax=ax, color='none', edgecolor='blue', linewidth=2, label="Alpha Shape")

    # LIDAR başlangıç noktasını ve vektörünü çiz
    ax.scatter(*lidar_start_point, color='red', s=100, label="LIDAR Başlangıç")
    
    # LIDAR başlangıç vektörünü çiz
    ax.add_line(Line2D([lidar_start_point[0], lidar_vector[0]], 
                       [lidar_start_point[1], lidar_vector[1]], 
                       color='red', linewidth=2, label="LIDAR Vektörü"))

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
# ssh_download_file(hostname, username, password, remote_path, local_path)

# Veriyi oku ve temizle
data_temiz = read_and_clean_data(local_path)

# GeoDataFrame oluştur
gdf = create_geodataframe(data_temiz)

# Alpha Shape hesapla
alpha = 0.003 # Alfa parametresi, verilerinize göre ayarlayabilirsiniz
alpha_shape = calculate_alpha_shape(gdf, alpha)

# LIDAR başlangıç noktası
lidar_start_point = (0, 0)

# LIDAR başlangıç vektörü
ilk_nokta = (gdf.iloc[0].x, gdf.iloc[0].y)
lidar_vector = ilk_nokta

cizgi_mesafe = 10  # Çizgiye yakın mesafe örnek olarak 0.1 birim

# İlk nokta koordinatlarını yazdır
print(f"İlk nokta koordinatları: {ilk_nokta}")

# Haritayı çiz
plot_data_with_alpha_shape(gdf, lidar_start_point, lidar_vector, alpha_shape, cizgi_mesafe)
