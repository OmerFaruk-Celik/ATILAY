import cv2

def find_camera_ids(max_id=10):
    valid_camera_ids = []
    
    for camera_id in range(max_id):
        cap = cv2.VideoCapture(camera_id)
        if cap.isOpened():
            valid_camera_ids.append(camera_id)
            cap.release()
    
    return camera_id,valid_camera_ids

if __name__ == "__main__":
    camera_id,camera_ids = find_camera_ids()
    if camera_ids:
        print("Bağlı kameraların ID'leri:", camera_ids)
    else:
        print(camera_id," Kamera bulunamadı.")
