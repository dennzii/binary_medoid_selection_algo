#import cv2
import os
import math
import pydicom
import matplotlib.pyplot as plt
import numpy as np
from area_calc import getArea

slices_indices = []

TARGET_SHAPE = 15


sub_list_limit = 0

def get_binary_selected_indices(data, TARGET_SHAPE = TARGET_SHAPE):

    total_num_img = len(data)

    print(sub_list_limit)
    def recursive_binary_selection(data, sublist, offset):
        if len(sublist) > sub_list_limit and len(slices_indices) < TARGET_SHAPE:
            data_medoid_index, inner_medoid_index = find_medoid(data, sublist,offset)

            # Medoid indeksini slices_indices'e ekle
            if data_medoid_index not in slices_indices:
                slices_indices.append(data_medoid_index)

            # Sol grup için recursive çağrı
            recursive_binary_selection(data, sublist[:inner_medoid_index], offset)

            # Sağ grup için recursive çağrı
            recursive_binary_selection(data, sublist[inner_medoid_index + 1:], offset + inner_medoid_index + 1)

    def find_medoid(data, sublist,offset):
        # Listenin ortalamasını hesapla
        average = sum(sublist) / len(sublist)

        # Ortalamaya en yakın değeri bul
        medoid = min(sublist, key=lambda x: abs(x - average))

        # Medoid'in orijinal ve alt listedeki indekslerini bul
        data_medoid_index = data[offset:].index(medoid) +offset
        inner_medoid_index = sublist.index(medoid)

        return data_medoid_index, inner_medoid_index

    # Örnek veri

    # En büyük elemanı bul ve listeyi ikiye böl
    biggest_index = data.index(max(data))
    slices_indices.append(biggest_index)
    left = data[:biggest_index]
    right = data[biggest_index + 1:]

    # Sol ve sağ alt gruplar için recursive medoid hesaplama
    recursive_binary_selection(data, left, 0)
    recursive_binary_selection(data, right, biggest_index + 1)

    slices_indices.sort()

    return slices_indices


def load_dicom(path):
    dicom = pydicom.read_file(path)
    data = dicom.pixel_array
    data = data - np.min(data)
    if np.max(data) != 0:
        data = data / np.max(data)
    data = (data * 255).astype(np.uint8)
    return data


full_mri_list = []
def images_to_area_dict(path):#path ve area olarak bir dictionary döndürür.
    slice_area_list = []
    file_list = os.listdir(path)
    file_list.sort(key=lambda x: int(x.split('-')[1].split('.')[0]))
    for img_path in file_list:
        tmp_path = os.path.join(path, img_path)
        img = load_dicom(tmp_path)
        area = getArea(img)
        #eğer alan 0'sa direkt listeye ekleme.
        full_mri_list.append({"img_path": img_path, "area": area})
        if area != 0:
            slice_area_list.append({"img_path": img_path, "area": area})

    return slice_area_list

data = images_to_area_dict("FLAIR")
#get_binary_selected_indices(,20)

#area sutununu al
area_column = [item['area'] for item in data]

#ona gore seçilen fotoğrafların indislerini al
total_num_img = len(data)
print(len(data))
sub_list_limit = math.ceil((total_num_img - TARGET_SHAPE) / (TARGET_SHAPE + 1))
print(sub_list_limit)

get_binary_selected_indices(area_column,TARGET_SHAPE)

#ardından o indislerdeki elemanlardan oluşan liste altkümesini oluştur.
selected_data = [data[i] for i in slices_indices]

for d in selected_data:
    print(d)

print("=================")
for d in full_mri_list:
    print(d)

#Bazı slicelar zero. bunları bence yok etmeliyiz. ++
# Slicelar gerçekten sıralı mı? ++