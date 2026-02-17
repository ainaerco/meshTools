/**
 * @file chull.h
 * @brief 3D convex hull via incremental construction (double-triangle /
 * O'Rourke)
 */

#pragma once

#include <geometry/vector.h>
#include <memory>
#include <vector>

namespace meshTools {
namespace Chull {

struct ChullVertex;
struct ChullEdge;
struct ChullFace;

struct ChullVertex {
    Geometry::Vector v;
    int vnum = 0;
    ChullEdge *duplicate = nullptr;
    bool onHull = false;
    bool mark = false;
};

struct ChullEdge {
    ChullFace *adjFace[2] = {nullptr, nullptr};
    ChullVertex *endPts[2] = {nullptr, nullptr};
    ChullFace *newFace = nullptr;
    bool remove = false;
};

struct ChullFace {
    ChullEdge *edge[3] = {nullptr, nullptr, nullptr};
    ChullVertex *vertex[3] = {nullptr, nullptr, nullptr};
    bool visible = false;
};

/** Return true if a, b, c are collinear (cross product zero). */
bool collinear(const ChullVertex *a, const ChullVertex *b,
               const ChullVertex *c);

/**
 * Convex hull of a 3D point set.
 * Builds hull in constructor; use exportHull() to get [faces, vertices].
 */
class Hull {
  public:
    /**
     * Build convex hull from point set.
     * @param points Input points (Vector or equivalent)
     * @throws std::runtime_error if all points are collinear or coplanar
     */
    explicit Hull(const std::vector<Geometry::Vector> &points);

    Hull(const Hull &) = delete;
    Hull &operator=(const Hull &) = delete;
    Hull(Hull &&) = default;
    Hull &operator=(Hull &&) = default;

    /**
     * Return hull as mesh-ready data.
     * @return Pair of (faces, vertices): faces are triplets of vertex indices,
     *         vertices are hull vertices as Vector.
     */
    std::pair<std::vector<std::vector<int>>, std::vector<Geometry::Vector>>
    exportHull() const;

  private:
    std::vector<std::unique_ptr<ChullVertex>> vertices_;
    std::vector<std::unique_ptr<ChullEdge>> edges_;
    std::vector<std::unique_ptr<ChullFace>> faces_;

    static int volumeSign(const ChullFace *f, const ChullVertex *p);
    size_t doubleTriangle();
    void constructHull(size_t startV);
    void edgeOrderOnFaces();
    void addOne(ChullVertex *p);
    ChullFace *makeConeFace(ChullEdge *e, ChullVertex *p);
    std::pair<size_t, size_t> cleanUp(size_t ev, size_t v);
    void cleanEdges();
    void cleanFaces();
    std::pair<size_t, size_t> cleanVertices(size_t evi, size_t vi);
};

} // namespace Chull
} // namespace meshTools
