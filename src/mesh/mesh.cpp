#include "mesh.h"

namespace meshTools {
namespace Mesh {

float Vert::dot(const Vert &other) { return v.dot(other.v); }

Vector Vert::cross(const Vert &other) { return v.cross(other.v); }

std::vector<Vert *> Vert::neighbors() {
    std::vector<Vert *> n;
    for (int i = 0; i < edges.size(); i++) {
        n.push_back(edges[i]->verts[0]);
        n.push_back(edges[i]->verts[1]);
    }
    // n.group_duplicates();
    // int f = n.find(v);
    // n.erase(f);
    return n;
}

Vector Vert::computeNormal() {
    std::vector<Vert *> n = neighbors();
    Vector v1, v2, normal;
    for (int i = 0; i < n.size() - 1; i++) {
        v1 = v - n[i]->v;
        v2 = n[i + 1]->v - v;
        normal += v1.cross(v2);
    }
    normal = normal.normalize();
    return normal;
}

Vector Edge::computeNormal() {
    Vector normal;
    for (size_t i = 0; i < faces.size(); i++) {
        normal += faces[i]->normal;
    }
    normal = normal.normalize();
    return normal;
}

std::vector<Vert *> Face::toPairs() {
    std::vector<Vert *> pairs;
    size_t vsize = verts.size();

    for (size_t i = 0; i < vsize; i++) {
        if (i == vsize - 1) {
            pairs.push_back(verts[i]);
            pairs.push_back(verts[0]);
        } else {
            pairs.push_back(verts[i]);
            pairs.push_back(verts[i + 1]);
        }
    }
    return pairs;
}

bool Face::isPointInside(Vector v) { return true; }

Vector Face::computeNormal() {
    Vector normal;
    size_t vsize = verts.size();
    for (size_t i = 0; i < vsize; i++) {
        if (i == vsize - 1) {
            normal += verts[i]->cross(*verts[0]);
        } else {
            normal += verts[i]->cross(*verts[i + 1]);
        }
    }
    normal = normal.normalize();
    return normal;
}

Vector Face::computeCenter() {
    Vector center;
    size_t vsize = verts.size();
    for (size_t i = 0; i < vsize; i++) {
        center += verts[i]->v;
    }
    center /= static_cast<float>(vsize);
    return center;
}

} // namespace Mesh
} // namespace meshTools