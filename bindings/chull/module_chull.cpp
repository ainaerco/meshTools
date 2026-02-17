#include <chull/chull.h>
#include <geometry/vector.h>
#include <nanobind/nanobind.h>
#include <nanobind/stl/vector.h>

namespace nb = nanobind;
using namespace nb::literals;

namespace meshTools {
namespace Chull {

void exportChullModule(nb::module_ &m) {
    nb::class_<Hull>(m, "Hull",
                     "Convex hull of a 3D point set. Use exportHull() for "
                     "[faces, vertices].")
        .def(nb::init<const std::vector<Geometry::Vector> &>(), "v"_a,
             "Build convex hull from list of Vector points.")
        .def(
            "exportHull",
            [](const Hull &h) {
                auto [faces, vertices] = h.exportHull();
                nb::list pyFaces;
                for (const auto &tri : faces) {
                    nb::list pyTri;
                    for (int idx : tri)
                        pyTri.append(idx);
                    pyFaces.append(pyTri);
                }
                nb::list pyVertices;
                for (const auto &v : vertices)
                    pyVertices.append(v);
                return nb::make_tuple(pyFaces, pyVertices);
            },
            "Return [faces, vertices]: faces are [[v0,v1,v2], ...], vertices "
            "are Vector.");
}

} // namespace Chull
} // namespace meshTools

NB_MODULE(_chull, m) { meshTools::Chull::exportChullModule(m); }
