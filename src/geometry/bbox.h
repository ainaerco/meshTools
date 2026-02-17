/**
 * @file bbox.h
 * @brief Bounding box class for spatial calculations
 */

#ifndef _MESHTOOLS_BBOX_H
#define _MESHTOOLS_BBOX_H

#include <geometry/vector.h>

namespace meshTools {
namespace Geometry {

/**
 * @class Bbox
 * @brief A bounding box class for spatial calculations
 *
 * This class represents an axis-aligned or oriented bounding box (OBB)
 * defined by minimum and maximum points, with optional center and axis information.
 */
class Bbox {
  public:
    /** @brief Default constructor */
    Bbox() {}
    
    /**
     * @brief Construct bounding box from min and max points
     * @param mn Minimum point
     * @param mx Maximum point
     */
    Bbox(const Vector &mn, const Vector &mx) : min(mn), max(mx) {}
    
    /**
     * @brief Construct bounding box from min, max, and center points
     * @param mn Minimum point
     * @param mx Maximum point
     * @param c Center point
     */
    Bbox(const Vector &mn, const Vector &mx, const Vector &c)
        : min(mn), max(mx), center(c) {}
    
    Vector min;      ///< Minimum point of the bounding box
    Vector max;      ///< Maximum point of the bounding box
    Vector center;   ///< Center point of the bounding box
    Vector axis[3];  ///< Axis vectors for oriented bounding box
    
    /**
     * @brief Compute axis-aligned bounding box from a set of points
     * @param pointset Set of points to compute bounding box from
     */
    void fromPointSet(const std::vector<Vector> &pointset);
    
    /**
     * @brief Compute oriented bounding box (OBB) from a set of points
     * @param pointset Set of points to compute OBB from
     */
    void obbFromPointSet(const std::vector<Vector> &pointset);
    
    /**
     * @brief Calculate the center point of the bounding box
     */
    void calcCenter();

    /**
     * @brief Array subscript operator for accessing bbox properties
     * @param index Index (0=min, 1=max, 2=center)
     * @return Vector at the specified index
     * @throws const char* if index is out of range
     */
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