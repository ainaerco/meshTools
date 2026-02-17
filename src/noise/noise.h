/**
 * @file noise.h
 * @brief Simplex-style procedural noise (2D, 3D, 4D)
 */

#pragma once

#include <cmath>
#include <vector>

namespace meshTools {
namespace Noise {

/**
 * Procedural Simplex-style noise generator (2D, 3D, 4D).
 * Values in [-1, 1] unless noted.
 */
class Noise {
  public:
    Noise() = default;

    /** Scalar noise 2D. */
    float snoise(float x, float y) const;
    /** Scalar noise 3D. */
    float snoise(float x, float y, float z) const;
    /** Scalar noise 4D. */
    float snoise(float x, float y, float z, float t) const;

    /** Vector noise 2D -> (ox, oy). */
    void vsnoise(float x, float y, float &ox, float &oy) const;
    /** Vector noise 3D -> (ox, oy, oz). */
    void vsnoise(float x, float y, float z, float &ox, float &oy,
                 float &oz) const;
    /** Vector noise 4D -> (ox, oy, oz, ot). */
    void vsnoise(float x, float y, float z, float t, float &ox, float &oy,
                 float &oz, float &ot) const;

    /** Fractional Brownian motion (3D); returns value in [0, 1]. */
    float fBm(float x, float y, float z, int octaves, float lacunarity,
              float gain) const;
    /** Turbulence (3D); returns value in [0, 1]. */
    float turbulence(float x, float y, float z, int octaves, float lacunarity,
                     float gain) const;
    /** Vector fBm (3D). */
    void vfBm(float x, float y, float z, int octaves, float lacunarity,
              float gain, float &ox, float &oy, float &oz) const;
    /** Vector turbulence (3D). */
    void vturbulence(float x, float y, float z, int octaves, float lacunarity,
                     float gain, float &ox, float &oy, float &oz) const;

  private:
    static int tabindex2(int ix, int iy);
    static int tabindex3(int ix, int iy, int iz);
    static int tabindex4(int ix, int iy, int iz, int it);
    float noise2d(float x, float y) const;
    float noise3d(float x, float y, float z) const;
    float noise4d(float x, float y, float z, float t) const;
};

} // namespace Noise
} // namespace meshTools
