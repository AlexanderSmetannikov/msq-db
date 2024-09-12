#include <vector>
#include <cnpy.h>
#include <cuda_runtime.h>
#include <limits>
// CUDA ядро для вычисления расстояний и нахождения ближайших соседей
__global__ void find_nearest_neighbors(const float* query, const float* database, int* indices, float* distances, int num_db, int dim, int num_neighbors) {
    int db_idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (db_idx < num_db) {
        float dist = 0.0f;
        for (int i = 0; i < dim; ++i) {
            float diff = query[i] - database[db_idx * dim + i];
            dist += diff * diff;
        }
        dist = sqrtf(dist);

        // Update nearest neighbors
        for (int k = 0; k < num_neighbors; ++k) {
            if (dist < distances[k] || distances[k] < 0) {
                // Shift the rest
                for (int l = num_neighbors - 1; l > k; --l) {
                    distances[l] = distances[l - 1];
                    indices[l] = indices[l - 1];
                }
                // Insert the new distance
                distances[k] = dist;
                indices[k] = db_idx;
                break;
            }
        }
    }
}


// Функция для загрузки данных из .npy файла и передачи на GPU
void load_data_to_gpu(const std::string& filename, float** d_data, size_t num_elements) {
    // Загрузка данных из .npy файла
    cnpy::NpyArray arr = cnpy::npy_load(filename);
    float* h_data = arr.data<float>();

    // Выделение памяти на GPU
    cudaMalloc(d_data, num_elements * sizeof(float));
    // Копирование данных с CPU на GPU
    cudaMemcpy(*d_data, h_data, num_elements * sizeof(float), cudaMemcpyHostToDevice);
}

// Основная функция для выполнения поиска ближайших соседей
void find_nearest_neighbors_gpu(const std::string& query_file, const std::string& database_file, std::vector<int>& indices, std::vector<float>& distances, int num_db, int dim, int num_neighbors) {
    float* d_query;
    float* d_database;
    int* d_indices;
    float* d_distances;

    size_t query_size = dim;
    size_t database_size = num_db * dim;
    size_t indices_size = num_neighbors * sizeof(int);
    size_t distances_size = num_neighbors * sizeof(float);

    // Загрузка данных на GPU
    load_data_to_gpu(query_file, &d_query, query_size);
    load_data_to_gpu(database_file, &d_database, database_size);

    // Выделение памяти для результатов на GPU
    cudaMalloc(&d_indices, indices_size);
    cudaMalloc(&d_distances, distances_size);

    // Инициализация расстояний на GPU значением инфинити
    std::vector<float> init_distances(num_neighbors, std::numeric_limits<float>::infinity());
    cudaMemcpy(d_distances, init_distances.data(), distances_size, cudaMemcpyHostToDevice);

    int block_size = 256;
    int grid_size = (num_db + block_size - 1) / block_size;
    find_nearest_neighbors<<<grid_size, block_size>>>(d_query, d_database, d_indices, d_distances, num_db, dim, num_neighbors);

    // Проверка на ошибки в запуске ядра
    cudaError_t error = cudaGetLastError();
    if (error != cudaSuccess) {
        std::cerr << "CUDA error: " << cudaGetErrorString(error) << std::endl;
    }

    // Копирование результатов обратно на CPU
    cudaMemcpy(indices.data(), d_indices, indices_size, cudaMemcpyDeviceToHost);
    cudaMemcpy(distances.data(), d_distances, distances_size, cudaMemcpyDeviceToHost);

    // Освобождение памяти на GPU
    cudaFree(d_query);
    cudaFree(d_database);
    cudaFree(d_indices);
    cudaFree(d_distances);
}

int main() {
    const int d = 1024;  // Размерность векторов
    const int nb = 27000; // Количество векторов в базе данных
    const int k = 4;     // Количество ближайших соседей

    std::vector<int> indices(k);
    std::vector<float> distances(k);

    // Поиск ближайших соседей
    find_nearest_neighbors_gpu("../query.npy", "../vecs.npy", indices, distances, nb, d, k);

    // Вывод результатов (индексы и расстояния ближайших соседей)
    std::cout << "Nearest neighbors:\n";
    for (int j = 0; j < k; ++j) {
        std::cout << "Index: " << indices[j] << ", Distance: " << distances[j] << "\n";
    }

    return 0;
}