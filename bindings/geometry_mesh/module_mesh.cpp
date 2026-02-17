#include <cstddef>
#include <cstdint>

#include <nanobind/nanobind.h>
#include <nanobind/stl/vector.h>

#include <mesh/mesh.h>

namespace nb = nanobind;

using namespace meshTools::Mesh;

void export_mesh_module(nb::module_ &m) {
    nb::class_<Vert>(m, "Vert")
        .def(nb::init<>())
        .def("computeNormal", &Vert::computeNormal);

    nb::class_<Mesh>(m, "Mesh")
        .def(nb::init<>())
        .def_prop_ro("verts", [](const Mesh &mesh) { return mesh.verts; });
}

NB_MODULE(_mesh, m) { export_mesh_module(m); }
