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
    : mPoints(points), mIndices(indices), mNormal(normal) {
    mSize = mIndices.size();
}

// Triangulate simple polygon using minimum angle ear clipping algorithm
std::vector<int> Polygon::triangulate() const {
    std::vector<int> resultIndices;
    float maxDot = 0.0f;
    size_t index = 0;
    for (size_t i = 1; i < mSize; ++i) {
        Vector edge0 = mPoints[mIndices[i]] - mPoints[mIndices[i - 1]];
        Vector edge1 =
            mPoints[mIndices[i]] - mPoints[mIndices[(i + 1) % mSize]];
        edge0 = edge0.normalize();
        edge1 = edge1.normalize();
        float dot = edge0.dot(edge1);
        Vector normal = edge0.cross(edge1);

        if (dot > maxDot && normal.dot(mNormal) < 0) {
            index = i;
            maxDot = dot;
        }
    }
    const size_t first = (int)index - 1 < 0 ? mSize - 1 : index - 1;
    resultIndices.push_back(mIndices[first]);
    resultIndices.push_back(mIndices[index]);
    resultIndices.push_back(mIndices[(index + 1) % mSize]);
    if (mIndices.size() > 3) {
        std::vector<int> indices(mIndices);
        indices.erase(indices.begin() + index);
        const Polygon poly(mPoints, indices, mNormal);
        const std::vector<int> triIndices = poly.triangulate();
        resultIndices.insert(resultIndices.end(), triIndices.begin(),
                             triIndices.end());
    }
    return resultIndices;
}

} // namespace Geometry
} // namespace meshTools
