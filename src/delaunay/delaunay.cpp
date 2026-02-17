/**
 * @file delaunay.cpp
 * @brief Implementation of 3D Delaunay tetrahedralization
 */

#include <cmath>
#include <delaunay/delaunay.h>
#include <geometry/vector.h>

namespace meshTools {
namespace Delaunay {

namespace {

float det3(const float a[3][3]) {
    return a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1]) -
           a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0]) +
           a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]);
}

} // namespace

float det4(const float m[4][4]) {
    float s1[3][3] = {{m[1][1], m[1][2], m[1][3]},
                      {m[2][1], m[2][2], m[2][3]},
                      {m[3][1], m[3][2], m[3][3]}};
    float s2[3][3] = {{m[0][1], m[0][2], m[0][3]},
                      {m[2][1], m[2][2], m[2][3]},
                      {m[3][1], m[3][2], m[3][3]}};
    float s3[3][3] = {{m[0][1], m[0][2], m[0][3]},
                      {m[1][1], m[1][2], m[1][3]},
                      {m[3][1], m[3][2], m[3][3]}};
    float s4[3][3] = {{m[0][1], m[0][2], m[0][3]},
                      {m[1][1], m[1][2], m[1][3]},
                      {m[2][1], m[2][2], m[2][3]}};
    return m[0][0] * det3(s1) - m[1][0] * det3(s2) + m[2][0] * det3(s3) -
           m[3][0] * det3(s4);
}

void Delaunay::calculateCircumsphere(
    Tetra &t, const std::vector<Geometry::Vector> &verts) {
    const Geometry::Vector &v0 = verts[t.v[0]];
    const Geometry::Vector &v1 = verts[t.v[1]];
    const Geometry::Vector &v2 = verts[t.v[2]];
    const Geometry::Vector &v3 = verts[t.v[3]];
    float v0_len = v0.x * v0.x + v0.y * v0.y + v0.z * v0.z;
    float v1_len = v1.x * v1.x + v1.y * v1.y + v1.z * v1.z;
    float v2_len = v2.x * v2.x + v2.y * v2.y + v2.z * v2.z;
    float v3_len = v3.x * v3.x + v3.y * v3.y + v3.z * v3.z;
    float a = 2.f * t.determinant;
    float m0[4][4] = {{v0_len, v0.y, v0.z, 1.f},
                      {v1_len, v1.y, v1.z, 1.f},
                      {v2_len, v2.y, v2.z, 1.f},
                      {v3_len, v3.y, v3.z, 1.f}};
    float m1[4][4] = {{v0_len, v0.x, v0.z, 1.f},
                      {v1_len, v1.x, v1.z, 1.f},
                      {v2_len, v2.x, v2.z, 1.f},
                      {v3_len, v3.x, v3.z, 1.f}};
    float m2[4][4] = {{v0_len, v0.x, v0.y, 1.f},
                      {v1_len, v1.x, v1.y, 1.f},
                      {v2_len, v2.x, v2.y, 1.f},
                      {v3_len, v3.x, v3.y, 1.f}};
    float d0 = det4(m0);
    float d1 = -det4(m1);
    float d2 = det4(m2);
    t.circumcenter.x = d0 / a;
    t.circumcenter.y = d1 / a;
    t.circumcenter.z = d2 / a;
    Geometry::Vector diff = t.circumcenter - v0;
    t.circumradius =
        std::sqrt(diff.x * diff.x + diff.y * diff.y + diff.z * diff.z);
}

void Delaunay::addTetrahedra(size_t vIndex, size_t tetraIndex, int caseVal) {
    if (caseVal != 0)
        return;
    const Tetra &t = tetras_[tetraIndex];
    size_t v0 = t.v[0], v1 = t.v[1], v2 = t.v[2], v3 = t.v[3];
    Tetra nt0, nt1, nt2, nt3;
    nt0.v[0] = v0;
    nt0.v[1] = v1;
    nt0.v[2] = v2;
    nt0.v[3] = vIndex;
    nt1.v[0] = v0;
    nt1.v[1] = v1;
    nt1.v[2] = vIndex;
    nt1.v[3] = v3;
    nt2.v[0] = v0;
    nt2.v[1] = vIndex;
    nt2.v[2] = v2;
    nt2.v[3] = v3;
    nt3.v[0] = vIndex;
    nt3.v[1] = v1;
    nt3.v[2] = v2;
    nt3.v[3] = v3;
    float m0[4][4] = {
        {vertices_[v0].x, vertices_[v0].y, vertices_[v0].z, 1.f},
        {vertices_[v1].x, vertices_[v1].y, vertices_[v1].z, 1.f},
        {vertices_[v2].x, vertices_[v2].y, vertices_[v2].z, 1.f},
        {vertices_[vIndex].x, vertices_[vIndex].y, vertices_[vIndex].z, 1.f}};
    float m1[4][4] = {
        {vertices_[v0].x, vertices_[v0].y, vertices_[v0].z, 1.f},
        {vertices_[v1].x, vertices_[v1].y, vertices_[v1].z, 1.f},
        {vertices_[vIndex].x, vertices_[vIndex].y, vertices_[vIndex].z, 1.f},
        {vertices_[v3].x, vertices_[v3].y, vertices_[v3].z, 1.f}};
    float m2[4][4] = {
        {vertices_[v0].x, vertices_[v0].y, vertices_[v0].z, 1.f},
        {vertices_[vIndex].x, vertices_[vIndex].y, vertices_[vIndex].z, 1.f},
        {vertices_[v2].x, vertices_[v2].y, vertices_[v2].z, 1.f},
        {vertices_[v3].x, vertices_[v3].y, vertices_[v3].z, 1.f}};
    float m3[4][4] = {
        {vertices_[vIndex].x, vertices_[vIndex].y, vertices_[vIndex].z, 1.f},
        {vertices_[v1].x, vertices_[v1].y, vertices_[v1].z, 1.f},
        {vertices_[v2].x, vertices_[v2].y, vertices_[v2].z, 1.f},
        {vertices_[v3].x, vertices_[v3].y, vertices_[v3].z, 1.f}};
    nt0.determinant = det4(m0);
    nt1.determinant = det4(m1);
    nt2.determinant = det4(m2);
    nt3.determinant = det4(m3);
    calculateCircumsphere(nt0, vertices_);
    calculateCircumsphere(nt1, vertices_);
    calculateCircumsphere(nt2, vertices_);
    calculateCircumsphere(nt3, vertices_);
    nt0.parent = tetraIndex;
    nt1.parent = tetraIndex;
    nt2.parent = tetraIndex;
    nt3.parent = tetraIndex;
    tetras_.push_back(nt0);
    tetras_.push_back(nt1);
    tetras_.push_back(nt2);
    tetras_.push_back(nt3);
}

void Delaunay::pointInTetrahedra(size_t vIndex, size_t tetraIndex) {
    const Tetra &tetra = tetras_[tetraIndex];
    size_t v0 = tetra.v[0], v1 = tetra.v[1], v2 = tetra.v[2], v3 = tetra.v[3];
    float d = tetra.determinant;
    const Geometry::Vector &pv = vertices_[vIndex];
    const Geometry::Vector &p0 = vertices_[v0];
    const Geometry::Vector &p1 = vertices_[v1];
    const Geometry::Vector &p2 = vertices_[v2];
    const Geometry::Vector &p3 = vertices_[v3];
    float mat0[4][4] = {{pv.x, pv.y, pv.z, 1.f},
                        {p1.x, p1.y, p1.z, 1.f},
                        {p2.x, p2.y, p2.z, 1.f},
                        {p3.x, p3.y, p3.z, 1.f}};
    float mat1[4][4] = {{p0.x, p0.y, p0.z, 1.f},
                        {pv.x, pv.y, pv.z, 1.f},
                        {p2.x, p2.y, p2.z, 1.f},
                        {p3.x, p3.y, p3.z, 1.f}};
    float mat2[4][4] = {{p0.x, p0.y, p0.z, 1.f},
                        {p1.x, p1.y, p1.z, 1.f},
                        {pv.x, pv.y, pv.z, 1.f},
                        {p3.x, p3.y, p3.z, 1.f}};
    float mat3[4][4] = {{p0.x, p0.y, p0.z, 1.f},
                        {p1.x, p1.y, p1.z, 1.f},
                        {p2.x, p2.y, p2.z, 1.f},
                        {pv.x, pv.y, pv.z, 1.f}};
    float d0 = det4(mat0);
    float d1 = det4(mat1);
    float d2 = det4(mat2);
    float d3 = det4(mat3);
    if (d == 0.f) {
        return;
    }
    if ((d > 0.f && d0 > 0.f && d1 > 0.f && d2 > 0.f && d3 > 0.f) ||
        (d < 0.f && d0 < 0.f && d1 < 0.f && d2 < 0.f && d3 < 0.f)) {
        addTetrahedra(vIndex, tetraIndex, 0);
    }
}

Delaunay::Delaunay(const std::vector<Geometry::Vector> &vertices,
                   float maxVal) {
    orig_vertices_ = vertices;
    float k = 3.f * maxVal;
    vertices_.push_back(Geometry::Vector(k, 0.f, 0.f));
    vertices_.push_back(Geometry::Vector(-k, k, 0.f));
    vertices_.push_back(Geometry::Vector(0.f, 0.f, k));
    vertices_.push_back(Geometry::Vector(0.f, -2.f * k, 0.f));
    Tetra t0;
    t0.v[0] = 0;
    t0.v[1] = 1;
    t0.v[2] = 2;
    t0.v[3] = 3;
    float m[4][4] = {{vertices_[0].x, vertices_[0].y, vertices_[0].z, 1.f},
                     {vertices_[1].x, vertices_[1].y, vertices_[1].z, 1.f},
                     {vertices_[2].x, vertices_[2].y, vertices_[2].z, 1.f},
                     {vertices_[3].x, vertices_[3].y, vertices_[3].z, 1.f}};
    t0.determinant = det4(m);
    calculateCircumsphere(t0, vertices_);
    t0.parent = 0;
    tetras_.push_back(t0);
    for (const auto &vert : orig_vertices_) {
        vertices_.push_back(vert);
        size_t vi = vertices_.size() - 1;
        pointInTetrahedra(vi, 0);
    }
}

std::vector<std::vector<int>> Delaunay::getTetras() const {
    std::vector<std::vector<int>> out;
    for (const auto &t : tetras_) {
        out.push_back({static_cast<int>(t.v[0]), static_cast<int>(t.v[1]),
                       static_cast<int>(t.v[2]), static_cast<int>(t.v[3])});
    }
    return out;
}

} // namespace Delaunay
} // namespace meshTools
