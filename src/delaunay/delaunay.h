/**
 * @file delaunay.h
 * @brief 3D Delaunay tetrahedralization (incremental algorithm)
 */

#pragma once

#include <geometry/vector.h>
#include <vector>

namespace meshTools {
namespace Delaunay {

/** Determinant of a 4x4 matrix (row-major, 4 rows of 4 floats). */
float det4(const float m[4][4]);

/**
 * Tetrahedron with 4 vertex indices, determinant, circumcenter and
 * circumradius. Used internally during construction.
 */
struct Tetra {
    size_t v[4];
    float determinant = 0.f;
    Geometry::Vector circumcenter;
    float circumradius = 0.f;
    std::vector<size_t> child;
    size_t parent = 0; // index into tetras
};

/**
 * 3D Delaunay tetrahedralization built incrementally from a point set.
 * Starts from a bounding tetrahedron, inserts points, subdivides tetrahedra.
 */
class Delaunay {
  public:
    /**
     * Build Delaunay from point set.
     * @param vertices Input points
     * @param maxVal Used to construct bounding tetrahedron (k = 3*maxVal)
     */
    Delaunay(const std::vector<Geometry::Vector> &vertices, float maxVal);

    Delaunay(const Delaunay &) = delete;
    Delaunay &operator=(const Delaunay &) = delete;
    Delaunay(Delaunay &&) = default;
    Delaunay &operator=(Delaunay &&) = default;

    /** Original input vertices (unchanged). */
    const std::vector<Geometry::Vector> &getOrigVertices() const {
        return orig_vertices_;
    }
    /** All vertices (bounding + input). */
    const std::vector<Geometry::Vector> &getVertices() const {
        return vertices_;
    }
    /** Tetrahedra as 4-tuples of vertex indices. */
    std::vector<std::vector<int>> getTetras() const;

  private:
    std::vector<Geometry::Vector> orig_vertices_;
    std::vector<Geometry::Vector> vertices_;
    std::vector<Tetra> tetras_;

    void addTetrahedra(size_t vIndex, size_t tetraIndex, int caseVal);
    void pointInTetrahedra(size_t vIndex, size_t tetraIndex);
    static void
    calculateCircumsphere(Tetra &t, const std::vector<Geometry::Vector> &verts);
};

} // namespace Delaunay
} // namespace meshTools
