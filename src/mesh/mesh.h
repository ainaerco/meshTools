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

    float dot(const Vert &other);
    Vector cross(const Vert &other);
    std::vector<Vert *> neighbors();
    Vector computeNormal();
};

class Edge {
  public:
    Edge() {}

    unsigned int id;
    Vert *verts[2];
    std::vector<Face *> faces; // Face * f = new Face();

    Vector computeNormal();

    Vert *operator[](const size_t &index) { return verts[index]; }
};

class Face {
  public:
    Face() {}

    unsigned int id;
    std::vector<Vert *> verts;
    std::vector<Edge *> edges;
    Vector normal;

    std::vector<Vert *> toPairs();
    bool isPointInside(Vector v);
    Vector computeNormal();
    Vector computeCenter();

    Vert *operator[](const size_t &index) { return verts[index]; }
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