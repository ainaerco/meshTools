/**
 * @file polygon.cpp
 * @brief Implementation of polygon triangulation and operations
 */

#include <geometry/polygon.h>
#include <geometry/vector.h>

namespace meshTools {
namespace Geometry {

Polygon::Polygon(const std::vector<Vector> &points,
                 const std::vector<int> &indices, const Vector &normal)
    : m_points(points), m_indices(indices), m_normal(normal) {
    m_size = m_indices.size();
}

// Triangulate simple polygon using minimum angle ear clipping algorithm
std::vector<int> Polygon::triangulate() const {
    std::vector<int> resultIndices;
    float maxDot = 0.0f;
    size_t index = 0;
    for (size_t i = 1; i < m_size; ++i) {
        Vector edge0 = m_points[m_indices[i]] - m_points[m_indices[i - 1]];
        Vector edge1 =
            m_points[m_indices[i]] - m_points[m_indices[(i + 1) % m_size]];
        edge0 = edge0.normalize();
        edge1 = edge1.normalize();
        float dot = edge0.dot(edge1);
        Vector normal = edge0.cross(edge1);

        if (dot > maxDot && normal.dot(m_normal) < 0) {
            index = i;
            maxDot = dot;
        }
    }
    const size_t first = (int)index - 1 < 0 ? m_size - 1 : index - 1;
    resultIndices.push_back(m_indices[first]);
    resultIndices.push_back(m_indices[index]);
    resultIndices.push_back(m_indices[(index + 1) % m_size]);
    if (m_indices.size() > 3) {
        std::vector<int> indices(m_indices);
        indices.erase(indices.begin() + index);
        const Polygon poly(m_points, indices, m_normal);
        const std::vector<int> triIndices = poly.triangulate();
        resultIndices.insert(resultIndices.end(), triIndices.begin(),
                             triIndices.end());
    }
    return resultIndices;
}

} // namespace Geometry
} // namespace meshTools
