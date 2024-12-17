import sys
import struct
import numpy as np
import matplotlib.pyplot as plt #type: ignore
from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename


def read_binary_file(filename):
    with (open(filename, 'rb') as f):
        # Читаем заголовок
        header = f.readline().decode().strip().split('|')

        map_metadata = {
            'xlen': int(header[0]),                             # размер карты по ширине
            'ylen': int(header[1]),                             # размер карты по длине
            'stepx': float(header[2].replace(',', '.')),        # шаг по X 3.5
            'stepy': float(header[3].replace(',', '.')),        # шаг по Y 8
            'startx': int(header[4]),                           # начало данных по X
            'starty': int(header[5]),                           # начало данных по Y
            'lastx': int(header[6]),                            # конец данных по X
            'lasty': int(header[7]),                            # конец данных по Y
            'width': int(header[8]),                            # количество точек по ширине 371
            'height': int(header[9]),                           # количество точек по длине 784
            'baselevel': float(header[10].replace(',', '.'))    # базовый уровень
        }
        
        # Пропускаем заголовок
        f.seek(int(f.readline().decode().strip()))

        size = map_metadata['height'] * map_metadata['width']
        bytes = f.read(size * 4)  # 4 bytes на число с пл запятой?
        
        # Создаем матрицу для данных
        map_matrix = np.array(struct.unpack(f'{size}f', bytes)) / 10
        map_matrix += map_metadata['baselevel']

        # для imshow нужен 2D-array
        map_matrix = map_matrix.reshape(map_metadata['height'], map_metadata['width'])

    return map_metadata, map_matrix.transpose()


def analyze_data(map_metadata, map_matrix):
    plt.figure(figsize=(map_metadata['ylen']/50, map_metadata['xlen']/50))

    # x 0-6000, y 0-1200
    plt.imshow(
        map_matrix,
        cmap='hot',
        origin='lower',
        vmin=map_metadata['baselevel'],
        vmax=np.max(map_matrix),
        extent=[0, map_metadata['height'] * map_metadata['stepy'], 0, map_metadata['width'] * map_metadata['stepx']]
    )
    plt.title('Отклонения от горизонтали\n' + f'Dimensions: {map_metadata["xlen"]}x{map_metadata["ylen"]}' +
              f' ({map_metadata['width']}x{map_metadata['height']})\n' +
              f'X Step: {map_metadata["stepx"]}, Y Step: {map_metadata["stepy"]}\n' +
              f'X Range: {map_metadata["startx"]} to {map_metadata["lastx"]}, ' +
              f'Y Range: {map_metadata["starty"]} to {map_metadata["lasty"]}\n' +
              f'Base: {map_metadata['baselevel']}')
    plt.ylabel('Длина')
    plt.colorbar()
    plt.show()


def main():
    try:
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
        else:
            file_path = askopenfilename(
                initialdir="C:\\Users\\froli\\Labs\\Python\\6.1\\",
                title="Выберите файл .dat для обработки",
                defaultextension="dat",
                initialfile="data.dat"
            )

        map_metadata, map_matrix = read_binary_file(file_path)
        analyze_data(map_metadata, map_matrix)
    
    except FileNotFoundError as e:
        showerror('Ошибка','Файл не найден')
        quit()
    
    except IOError as e:
        showerror("Ошибка", f"Ошибка при чтении файла: {e}")
        quit()

    except Exception as e:
        showerror("Ошибка", str(e))


if __name__ == "__main__":
    main()
