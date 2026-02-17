#ifndef _MESHTOOLS_BBOX_H
#define _MESHTOOLS_BBOX_H

#include <geometry/vector.h>

namespace meshTools {
namespace Geometry {

class Bbox {
  public:
    Bbox() {}
    Bbox(const Vector &mn, const Vector &mx) : min(mn), max(mx) {}
    Bbox(const Vector &mn, const Vector &mx, const Vector &c)
        : min(mn), max(mx), center(c) {}
    Vector min;
    Vector max;
    Vector center;
    Vector axis[3];
    void fromPointSet(const std::vector<Vector> &pointset);
    void obbFromPointSet(const std::vector<Vector> &pointset);
    void calcCenter();

    Vector operator[](const size_t &index) const {
        if (index == 0) {
            return min;
        } else if (index == 1) {
            return max;
        } else if (index == 2) {
            return center;
        } else {
            throw "Index out of range";
        }
    }
};

} // namespace Geometry
} // namespace meshTools

#endif