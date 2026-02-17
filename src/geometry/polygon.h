#ifndef _MESHTOOLS_POLYGON_H
#define _MESHTOOLS_POLYGON_H
#include "geometry/vector.h"

namespace meshTools {
namespace Geometry {

class Polygon {
  public:
    Polygon(const std::vector<Vector> &points, std::vector<int> indices,
            Vector normal);
    std::vector<int> triangulate();

  private:
    std::vector<Vector> m_points;
    std::vector<int> m_indices;
    Vector m_normal;
    size_t m_size;
};

} // namespace Geometry
} // namespace meshTools
// _MESHTOOLS_POLYGON_H
#endif