#ifndef _MESHTOOLS_MESH_H
#define _MESHTOOLS_MESH_H

#include <geometry/bbox.h>
#include <geometry/vector.h>
#include <vector>

namespace meshTools {

namespace Mesh {

using namespace Geometry;

class Edge;
class Face;

class Vert {
  public:
    Vert() {}

    unsigned int id;
    Vector v;
    std::vector<Edge *> edges;
    std::vector<Face *> faces;

    float dot(const Vert &other) const;
    Vector cross(const Vert &other) const;
    std::vector<Vert *> neighbors() const;
    Vector computeNormal() const;
};

class Edge {
  public:
    Edge() {}

    unsigned int id;
    Vert *verts[2];
    std::vector<Face *> faces;

    Vector computeNormal() const;

    Vert *operator[](const size_t &index) { return verts[index]; }
    Vert *operator[](const size_t &index) const { return verts[index]; }
};

class Face {
  public:
    Face() {}

    unsigned int id;
    std::vector<Vert *> verts;
    std::vector<Edge *> edges;
    Vector normal;

    std::vector<Vert *> toPairs() const;
    bool isPointInside(const Vector &v) const;
    Vector computeNormal() const;
    Vector computeCenter() const;

    Vert *operator[](const size_t &index) { return verts[index]; }
    Vert *operator[](const size_t &index) const { return verts[index]; }
};

class Mesh {
  public:
    Mesh() { mode = "generic"; }

    std::string mode;
    std::vector<Vert *> verts;
    std::vector<Edge *> edges;
    std::vector<Face *> faces;
    Bbox bbox;
};

} // namespace Mesh
} // namespace meshTools

#endif