/**
 * @file chull.cpp
 * @brief Implementation of 3D convex hull (incremental construction)
 */

#include <algorithm>
#include <chull/chull.h>
#include <geometry/vector.h>
#include <memory>
#include <stdexcept>
#include <utility>

namespace meshTools {
namespace Chull {

namespace {

constexpr float kEpsilon = 1e-10f;

bool collinearImpl(const Geometry::Vector &a, const Geometry::Vector &b,
                   const Geometry::Vector &c) {
    float cx = (c.z - a.z) * (b.y - a.y) - (b.z - a.z) * (c.y - a.y);
    float cy = (b.z - a.z) * (c.x - a.x) - (b.x - a.x) * (c.z - a.z);
    float cz = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
    return (cx == 0.f && cy == 0.f && cz == 0.f);
}

void faceMakeCcw(ChullFace *f, ChullEdge *e, ChullVertex *p) {
    const ChullFace *fv = (e->adjFace[0] && e->adjFace[0]->visible)
                              ? e->adjFace[0]
                              : e->adjFace[1];
    size_t i = 0;
    while (fv->vertex[i] != e->endPts[0])
        ++i;
    if (fv->vertex[(i + 1) % 3] != e->endPts[1]) {
        f->vertex[0] = e->endPts[1];
        f->vertex[1] = e->endPts[0];
    } else {
        f->vertex[0] = e->endPts[0];
        f->vertex[1] = e->endPts[1];
        std::swap(f->edge[1], f->edge[2]);
    }
    f->vertex[2] = p;
}

} // namespace

bool collinear(const ChullVertex *a, const ChullVertex *b,
               const ChullVertex *c) {
    return collinearImpl(a->v, b->v, c->v);
}

int Hull::volumeSign(const ChullFace *f, const ChullVertex *p) {
    Geometry::Vector a = f->vertex[0]->v - p->v;
    Geometry::Vector b = f->vertex[1]->v - p->v;
    Geometry::Vector c = f->vertex[2]->v - p->v;
    float vol = a.x * (b.y * c.z - b.z * c.y) + a.y * (b.z * c.x - b.x * c.z) +
                a.z * (b.x * c.y - b.y * c.x);
    if (vol > kEpsilon)
        return 1;
    if (vol < -kEpsilon)
        return -1;
    return 0;
}

size_t Hull::doubleTriangle() {
    const size_t nv = vertices_.size();
    if (nv < 3)
        throw std::runtime_error("DoubleTriangle: need at least 3 points");

    size_t v0 = 0;
    while (collinear(vertices_[v0 % nv].get(), vertices_[(v0 + 1) % nv].get(),
                     vertices_[(v0 + 2) % nv].get())) {
        v0 = (v0 + 1) % nv;
        if (v0 == 0)
            throw std::runtime_error(
                "DoubleTriangle: All points are collinear!");
    }
    size_t v1 = (v0 + 1) % nv;
    size_t v2 = (v1 + 1) % nv;

    vertices_[v0]->mark = true;
    vertices_[v1]->mark = true;
    vertices_[v2]->mark = true;

    auto f0 = std::make_unique<ChullFace>();
    ChullFace *pf0 = f0.get();
    pf0->vertex[0] = vertices_[v0].get();
    pf0->vertex[1] = vertices_[v1].get();
    pf0->vertex[2] = vertices_[v2].get();

    auto e0 = std::make_unique<ChullEdge>();
    auto e1 = std::make_unique<ChullEdge>();
    auto e2 = std::make_unique<ChullEdge>();
    ChullEdge *pe0 = e0.get();
    ChullEdge *pe1 = e1.get();
    ChullEdge *pe2 = e2.get();
    pe0->endPts[0] = vertices_[v0].get();
    pe0->endPts[1] = vertices_[v1].get();
    pe1->endPts[0] = vertices_[v1].get();
    pe1->endPts[1] = vertices_[v2].get();
    pe2->endPts[0] = vertices_[v2].get();
    pe2->endPts[1] = vertices_[v0].get();
    pe0->adjFace[0] = pf0;
    pe1->adjFace[0] = pf0;
    pe2->adjFace[0] = pf0;
    pf0->edge[0] = pe0;
    pf0->edge[1] = pe1;
    pf0->edge[2] = pe2;
    faces_.emplace_back(std::move(f0));
    edges_.emplace_back(std::move(e0));
    edges_.emplace_back(std::move(e1));
    edges_.emplace_back(std::move(e2));

    auto f1 = std::make_unique<ChullFace>();
    ChullFace *pf1 = f1.get();
    pf1->vertex[0] = vertices_[v2].get();
    pf1->vertex[1] = vertices_[v1].get();
    pf1->vertex[2] = vertices_[v0].get();
    pf1->edge[0] = pe2;
    pf1->edge[1] = pe1;
    pf1->edge[2] = pe0;
    faces_.emplace_back(std::move(f1));
    pe0->adjFace[1] = pf1;
    pe1->adjFace[1] = pf1;
    pe2->adjFace[1] = pf1;

    size_t v3 = (v2 + 1) % nv;
    int vol = volumeSign(pf0, vertices_[v3].get());
    while (vol == 0) {
        v3 = (v3 + 1) % nv;
        if (v3 == 0)
            throw std::runtime_error(
                "DoubleTriangle: All points are coplanar!");
        vol = volumeSign(pf0, vertices_[v3].get());
    }

    return v3;
}

void Hull::constructHull(size_t startV) {
    size_t ev = startV;
    size_t v = startV;
    do {
        if (!vertices_[v]->mark)
            vertices_[v]->mark = true;
        addOne(vertices_[v].get());
        std::tie(ev, v) = cleanUp(ev, v);
        if (vertices_.empty())
            break;
    } while (v != ev);
}

void Hull::edgeOrderOnFaces() {
    for (auto &f : faces_) {
        for (int i = 0; i < 3; ++i) {
            ChullEdge *ei = f->edge[i];
            ChullVertex *vi = f->vertex[i];
            ChullVertex *vi1 = f->vertex[(i + 1) % 3];
            bool ok = (ei->endPts[0] == vi && ei->endPts[1] == vi1) ||
                      (ei->endPts[1] == vi && ei->endPts[0] == vi1);
            if (!ok) {
                for (int j = 0; j < 3; ++j) {
                    ChullEdge *ej = f->edge[j];
                    if ((ej->endPts[0] == vi && ej->endPts[1] == vi1) ||
                        (ej->endPts[1] == vi && ej->endPts[0] == vi1)) {
                        std::swap(f->edge[i], f->edge[j]);
                        break;
                    }
                }
            }
        }
    }
}

void Hull::addOne(ChullVertex *p) {
    bool vis = false;
    for (auto &f : faces_) {
        int vol = volumeSign(f.get(), p);
        if (vol < 0) {
            f->visible = true;
            vis = true;
        }
    }
    if (!vis) {
        p->onHull = false;
        return;
    }
    for (auto &e : edges_) {
        if (e->adjFace[0] && e->adjFace[1] && e->adjFace[0]->visible &&
            e->adjFace[1]->visible)
            e->remove = true;
        else if ((e->adjFace[0] && e->adjFace[0]->visible) ||
                 (e->adjFace[1] && e->adjFace[1]->visible))
            e->newFace = makeConeFace(e.get(), p);
    }
}

ChullFace *Hull::makeConeFace(ChullEdge *e, ChullVertex *p) {
    ChullEdge *newEdge[2] = {nullptr, nullptr};
    for (int i = 0; i < 2; ++i) {
        ChullEdge *d = e->endPts[i]->duplicate;
        if (!d) {
            auto ne = std::make_unique<ChullEdge>();
            ne->endPts[0] = e->endPts[i];
            ne->endPts[1] = p;
            e->endPts[i]->duplicate = ne.get();
            newEdge[i] = ne.get();
            edges_.push_back(std::move(ne));
        } else {
            newEdge[i] = d;
        }
    }
    auto newFace = std::make_unique<ChullFace>();
    newFace->edge[0] = e;
    newFace->edge[1] = newEdge[0];
    newFace->edge[2] = newEdge[1];
    faceMakeCcw(newFace.get(), e, p);
    ChullFace *fp = newFace.get();
    faces_.push_back(std::move(newFace));
    for (int i = 0; i < 2; ++i) {
        for (int j = 0; j < 2; ++j) {
            if (!newEdge[i]->adjFace[j]) {
                newEdge[i]->adjFace[j] = fp;
                break;
            }
        }
    }
    return fp;
}

std::pair<size_t, size_t> Hull::cleanUp(size_t ev, size_t v) {
    cleanEdges();
    cleanFaces();
    return cleanVertices(ev, v);
}

void Hull::cleanEdges() {
    for (auto &e : edges_) {
        if (e->newFace) {
            if (e->adjFace[0] && e->adjFace[0]->visible)
                e->adjFace[0] = e->newFace;
            else if (e->adjFace[1])
                e->adjFace[1] = e->newFace;
            e->newFace = nullptr;
        }
    }
    edges_.erase(std::remove_if(edges_.begin(), edges_.end(),
                                [](const std::unique_ptr<ChullEdge> &e) {
                                    return e->remove;
                                }),
                 edges_.end());
}

void Hull::cleanFaces() {
    faces_.erase(std::remove_if(faces_.begin(), faces_.end(),
                                [](const std::unique_ptr<ChullFace> &f) {
                                    return f->visible;
                                }),
                 faces_.end());
}

std::pair<size_t, size_t> Hull::cleanVertices(size_t evi, size_t vi) {
    for (auto &e : edges_) {
        e->endPts[0]->onHull = true;
        e->endPts[1]->onHull = true;
    }
    int viInt = static_cast<int>(vi);
    for (size_t i = 0; i < vertices_.size();) {
        ChullVertex *v = vertices_[i].get();
        if (v->mark && !v->onHull) {
            vertices_.erase(vertices_.begin() + static_cast<ptrdiff_t>(i));
            if (i < evi)
                --evi;
            --viInt;
        } else {
            ++i;
        }
    }
    for (auto &v : vertices_) {
        v->duplicate = nullptr;
        v->onHull = false;
    }
    size_t nv = vertices_.size();
    if (nv == 0)
        return {evi, 0};
    int nextV = (viInt + 1) % static_cast<int>(nv);
    if (nextV < 0)
        nextV += static_cast<int>(nv);
    return {evi, static_cast<size_t>(nextV)};
}

Hull::Hull(const std::vector<Geometry::Vector> &points) {
    for (size_t i = 0; i < points.size(); ++i) {
        auto vert = std::make_unique<ChullVertex>();
        vert->v = points[i];
        vert->vnum = static_cast<int>(i);
        vertices_.push_back(std::move(vert));
    }
    if (vertices_.size() < 3)
        return;
    if (vertices_.size() == 3) {
        if (collinear(vertices_[0].get(), vertices_[1].get(),
                      vertices_[2].get()))
            throw std::runtime_error(
                "DoubleTriangle: All points are collinear!");
        auto f0 = std::make_unique<ChullFace>();
        ChullFace *pf0 = f0.get();
        pf0->vertex[0] = vertices_[0].get();
        pf0->vertex[1] = vertices_[1].get();
        pf0->vertex[2] = vertices_[2].get();
        auto e0 = std::make_unique<ChullEdge>();
        auto e1 = std::make_unique<ChullEdge>();
        auto e2 = std::make_unique<ChullEdge>();
        ChullEdge *pe0 = e0.get();
        ChullEdge *pe1 = e1.get();
        ChullEdge *pe2 = e2.get();
        pe0->endPts[0] = vertices_[0].get();
        pe0->endPts[1] = vertices_[1].get();
        pe1->endPts[0] = vertices_[1].get();
        pe1->endPts[1] = vertices_[2].get();
        pe2->endPts[0] = vertices_[2].get();
        pe2->endPts[1] = vertices_[0].get();
        pe0->adjFace[0] = pf0;
        pe1->adjFace[0] = pf0;
        pe2->adjFace[0] = pf0;
        pf0->edge[0] = pe0;
        pf0->edge[1] = pe1;
        pf0->edge[2] = pe2;
        edges_.emplace_back(std::move(e0));
        edges_.emplace_back(std::move(e1));
        edges_.emplace_back(std::move(e2));
        faces_.emplace_back(std::move(f0));
        edgeOrderOnFaces();
        return;
    }
    size_t v3 = doubleTriangle();
    constructHull(v3);
    edgeOrderOnFaces();
}

std::pair<std::vector<std::vector<int>>, std::vector<Geometry::Vector>>
Hull::exportHull() const {
    std::vector<std::vector<int>> outFaces;
    std::vector<Geometry::Vector> outVertices;
    for (size_t i = 0; i < vertices_.size(); ++i)
        vertices_[i]->vnum = static_cast<int>(i);
    for (const auto &f : faces_) {
        outFaces.push_back(
            {f->vertex[0]->vnum, f->vertex[1]->vnum, f->vertex[2]->vnum});
    }
    for (const auto &vert : vertices_)
        outVertices.push_back(vert->v);
    return {outFaces, outVertices};
}

} // namespace Chull
} // namespace meshTools
