#ifndef _MESHTOOLS_POLYGON_H
#define _MESHTOOLS_POLYGON_H
#include "geometry/vector.h"

namespace meshTools {
namespace Geometry {

class Polygon {
  public:
    Polygon(const std::vector<Vector> &points, const std::vector<int> &indices,
            const Vector &normal);
    std::vector<int> triangulate() const;

  private:
    std::vector<Vector> m_points;
    std::vector<int> m_indices;
    Vector m_normal;
    size_t m_size;
};

} // namespace Geometry
} // namespace meshTools

#endif