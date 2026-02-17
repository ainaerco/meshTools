#include <nanobind/nanobind.h>
#include <noise/noise.h>

namespace nb = nanobind;
using namespace nb::literals;

namespace meshTools {
namespace Noise {

void export_noise_module(nb::module_ &m) {
    nb::class_<Noise>(m, "Noise",
                      "Procedural Simplex-style noise generator (2D, 3D, 4D).")
        .def(nb::init<>())
        .def("snoise",
             nb::overload_cast<float, float>(&Noise::snoise, nb::const_), "x"_a,
             "y"_a)
        .def("snoise",
             nb::overload_cast<float, float, float>(&Noise::snoise, nb::const_),
             "x"_a, "y"_a, "z"_a)
        .def("snoise",
             nb::overload_cast<float, float, float, float>(&Noise::snoise,
                                                           nb::const_),
             "x"_a, "y"_a, "z"_a, "t"_a)
        .def(
            "vsnoise",
            [](const Noise &n, float x, float y) {
                float ox, oy;
                n.vsnoise(x, y, ox, oy);
                return nb::make_tuple(ox, oy);
            },
            "x"_a, "y"_a)
        .def(
            "vsnoise",
            [](const Noise &n, float x, float y, float z) {
                float ox, oy, oz;
                n.vsnoise(x, y, z, ox, oy, oz);
                nb::list L;
                L.append(ox);
                L.append(oy);
                L.append(oz);
                return L;
            },
            "x"_a, "y"_a, "z"_a)
        .def(
            "vsnoise",
            [](const Noise &n, float x, float y, float z, float t) {
                float ox, oy, oz, ot;
                n.vsnoise(x, y, z, t, ox, oy, oz, ot);
                nb::list L;
                L.append(ox);
                L.append(oy);
                L.append(oz);
                L.append(ot);
                return L;
            },
            "x"_a, "y"_a, "z"_a, "t"_a)
        .def("fBm", &Noise::fBm, "x"_a, "y"_a, "z"_a, "octaves"_a,
             "lacunarity"_a, "gain"_a)
        .def("turbulence", &Noise::turbulence, "x"_a, "y"_a, "z"_a, "octaves"_a,
             "lacunarity"_a, "gain"_a)
        .def(
            "vfBm",
            [](const Noise &n, float x, float y, float z, int octaves,
               float lacunarity, float gain) {
                float ox, oy, oz;
                n.vfBm(x, y, z, octaves, lacunarity, gain, ox, oy, oz);
                nb::list L;
                L.append(ox);
                L.append(oy);
                L.append(oz);
                return L;
            },
            "x"_a, "y"_a, "z"_a, "octaves"_a, "lacunarity"_a, "gain"_a)
        .def(
            "vturbulence",
            [](const Noise &n, float x, float y, float z, int octaves,
               float lacunarity, float gain) {
                float ox, oy, oz;
                n.vturbulence(x, y, z, octaves, lacunarity, gain, ox, oy, oz);
                nb::list L;
                L.append(ox);
                L.append(oy);
                L.append(oz);
                return L;
            },
            "x"_a, "y"_a, "z"_a, "octaves"_a, "lacunarity"_a, "gain"_a);
}

} // namespace Noise
} // namespace meshTools

NB_MODULE(_noise, m) { meshTools::Noise::export_noise_module(m); }
