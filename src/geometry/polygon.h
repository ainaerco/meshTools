/**
 * @file polygon.h
 * @brief Polygon class for polygon operations
 */

#ifndef _MESHTOOLS_POLYGON_H
#define _MESHTOOLS_POLYGON_H
#include "geometry/vector.h"

namespace meshTools {
namespace Geometry {

/**
 * @class Polygon
 * @brief A polygon class for triangulation and polygon operations
 *
 * This class represents a polygon defined by a set of points, indices,
 * and a normal vector, supporting operations like triangulation.
 */
class Polygon {
  public:
    /**
     * @brief Construct a polygon from points, indices, and normal
     * @param points Set of vertices
     * @param indices Vertex indices defining the polygon
     * @param normal Normal vector of the polygon
     */
    Polygon(const std::vector<Vector> &points, const std::vector<int> &indices,
            const Vector &normal);
    
    /**
     * @brief Triangulate the polygon into triangles
     * @return Vector of indices forming triangles (each 3 indices form a triangle)
     */
    std::vector<int> triangulate() const;

  private:
    std::vector<Vector> m_points; ///< Vertex points of the polygon
    std::vector<int> m_indices;   ///< Vertex indices
    Vector m_normal;              ///< Normal vector of the polygon
    size_t m_size;                ///< Number of vertices in the polygon
};

} // namespace Geometry
} // namespace meshTools

#endif