/**
 * @file noise.cpp
 * @brief Implementation of Simplex-style procedural noise
 */

#include <noise/noise.h>
#include <noise/noise_tables.h>

namespace meshTools {
namespace Noise {

namespace {

constexpr int TABMASK = 0xFF;

inline int floor2int(float val) {
    int i = static_cast<int>(std::floor(val));
    return (val < 0.f && val != static_cast<float>(i)) ? i - 1 : i;
}

inline float lerp(float t, float a, float b) { return a + (b - a) * t; }

} // namespace

int Noise::tabindex2(int ix, int iy) {
    return perm[(ix + perm[iy & TABMASK]) & TABMASK];
}

int Noise::tabindex3(int ix, int iy, int iz) {
    return perm[(ix + perm[(iy + perm[iz & TABMASK]) & TABMASK]) & TABMASK];
}

int Noise::tabindex4(int ix, int iy, int iz, int it) {
    return perm[(it + perm[(ix + perm[(iy + perm[iz & TABMASK]) & TABMASK]) &
                           TABMASK]) &
                TABMASK];
}

float Noise::noise2d(float x, float y) const {
    int ix = floor2int(x), iy = floor2int(y);
    float rx0 = x - ix, ry0 = y - iy;
    float rx1 = rx0 - 1.f, ry1 = ry0 - 1.f;
    float sx = rx0 * rx0 * (3.f - 2.f * rx0);
    float sy = ry0 * ry0 * (3.f - 2.f * ry0);
    int i = tabindex2(ix, iy);
    float u = grads2[i][0] * rx0 + grads2[i][1] * ry0;
    i = tabindex2(ix + 1, iy);
    float v = grads2[i][0] * rx1 + grads2[i][1] * ry0;
    float a = lerp(sx, u, v);
    i = tabindex2(ix, iy + 1);
    u = grads2[i][0] * rx0 + grads2[i][1] * ry1;
    i = tabindex2(ix + 1, iy + 1);
    v = grads2[i][0] * rx1 + grads2[i][1] * ry1;
    float b = lerp(sx, u, v);
    return lerp(sy, a, b);
}

float Noise::noise3d(float x, float y, float z) const {
    int ix = floor2int(x), iy = floor2int(y), iz = floor2int(z);
    float rx0 = x - ix, ry0 = y - iy, rz0 = z - iz;
    float rx1 = rx0 - 1.f, ry1 = ry0 - 1.f, rz1 = rz0 - 1.f;
    float sx = rx0 * rx0 * (3.f - 2.f * rx0);
    float sy = ry0 * ry0 * (3.f - 2.f * ry0);
    float sz = rz0 * rz0 * (3.f - 2.f * rz0);
    int i = tabindex3(ix, iy, iz);
    float u = grads3[i][0] * rx0 + grads3[i][1] * ry0 + grads3[i][2] * rz0;
    i = tabindex3(ix + 1, iy, iz);
    float v = grads3[i][0] * rx1 + grads3[i][1] * ry0 + grads3[i][2] * rz0;
    float a = lerp(sx, u, v);
    i = tabindex3(ix, iy + 1, iz);
    u = grads3[i][0] * rx0 + grads3[i][1] * ry1 + grads3[i][2] * rz0;
    i = tabindex3(ix + 1, iy + 1, iz);
    v = grads3[i][0] * rx1 + grads3[i][1] * ry1 + grads3[i][2] * rz0;
    float b = lerp(sx, u, v);
    float c = lerp(sy, a, b);
    i = tabindex3(ix, iy, iz + 1);
    u = grads3[i][0] * rx0 + grads3[i][1] * ry0 + grads3[i][2] * rz1;
    i = tabindex3(ix + 1, iy, iz + 1);
    v = grads3[i][0] * rx1 + grads3[i][1] * ry0 + grads3[i][2] * rz1;
    a = lerp(sx, u, v);
    i = tabindex3(ix, iy + 1, iz + 1);
    u = grads3[i][0] * rx0 + grads3[i][1] * ry1 + grads3[i][2] * rz1;
    i = tabindex3(ix + 1, iy + 1, iz + 1);
    v = grads3[i][0] * rx1 + grads3[i][1] * ry1 + grads3[i][2] * rz1;
    b = lerp(sx, u, v);
    float d = lerp(sy, a, b);
    return lerp(sz, c, d);
}

float Noise::noise4d(float x, float y, float z, float t) const {
    int ix = floor2int(x), iy = floor2int(y), iz = floor2int(z),
        it = floor2int(t);
    float rx0 = x - ix, ry0 = y - iy, rz0 = z - iz, rt0 = t - it;
    float rx1 = rx0 - 1.f, ry1 = ry0 - 1.f, rz1 = rz0 - 1.f, rt1 = rt0 - 1.f;
    float sx = rx0 * rx0 * (3.f - 2.f * rx0);
    float sy = ry0 * ry0 * (3.f - 2.f * ry0);
    float sz = rz0 * rz0 * (3.f - 2.f * rz0);
    float st = rt0 * rt0 * (3.f - 2.f * rt0);
    int i = tabindex4(ix, iy, iz, it);
    float u = grads4[i][0] * rx0 + grads4[i][1] * ry0 + grads4[i][2] * rz0 +
              grads4[i][3] * rt0;
    i = tabindex4(ix + 1, iy, iz, it);
    float v = grads4[i][0] * rx1 + grads4[i][1] * ry0 + grads4[i][2] * rz0 +
              grads4[i][3] * rt0;
    float a = lerp(sx, u, v);
    i = tabindex4(ix, iy + 1, iz, it);
    u = grads4[i][0] * rx0 + grads4[i][1] * ry1 + grads4[i][2] * rz0 +
        grads4[i][3] * rt0;
    i = tabindex4(ix + 1, iy + 1, iz, it);
    v = grads4[i][0] * rx1 + grads4[i][1] * ry1 + grads4[i][2] * rz0 +
        grads4[i][3] * rt0;
    float b = lerp(sx, u, v);
    float c = lerp(sy, a, b);
    i = tabindex4(ix, iy, iz + 1, it);
    u = grads4[i][0] * rx0 + grads4[i][1] * ry0 + grads4[i][2] * rz1 +
        grads4[i][3] * rt0;
    i = tabindex4(ix + 1, iy, iz + 1, it);
    v = grads4[i][0] * rx1 + grads4[i][1] * ry0 + grads4[i][2] * rz1 +
        grads4[i][3] * rt0;
    a = lerp(sx, u, v);
    i = tabindex4(ix, iy + 1, iz + 1, it);
    u = grads4[i][0] * rx0 + grads4[i][1] * ry1 + grads4[i][2] * rz1 +
        grads4[i][3] * rt0;
    i = tabindex4(ix + 1, iy + 1, iz + 1, it);
    v = grads4[i][0] * rx1 + grads4[i][1] * ry1 + grads4[i][2] * rz1 +
        grads4[i][3] * rt0;
    b = lerp(sx, u, v);
    float d = lerp(sy, a, b);
    float e = lerp(sz, c, d);
    i = tabindex4(ix, iy, iz, it + 1);
    u = grads4[i][0] * rx0 + grads4[i][1] * ry0 + grads4[i][2] * rz0 +
        grads4[i][3] * rt1;
    i = tabindex4(ix + 1, iy, iz, it + 1);
    v = grads4[i][0] * rx1 + grads4[i][1] * ry0 + grads4[i][2] * rz0 +
        grads4[i][3] * rt1;
    a = lerp(sx, u, v);
    i = tabindex4(ix, iy + 1, iz, it + 1);
    u = grads4[i][0] * rx0 + grads4[i][1] * ry1 + grads4[i][2] * rz0 +
        grads4[i][3] * rt1;
    i = tabindex4(ix + 1, iy + 1, iz, it + 1);
    v = grads4[i][0] * rx1 + grads4[i][1] * ry1 + grads4[i][2] * rz0 +
        grads4[i][3] * rt1;
    b = lerp(sx, u, v);
    c = lerp(sy, a, b);
    i = tabindex4(ix, iy, iz + 1, it + 1);
    u = grads4[i][0] * rx0 + grads4[i][1] * ry0 + grads4[i][2] * rz1 +
        grads4[i][3] * rt1;
    i = tabindex4(ix + 1, iy, iz + 1, it + 1);
    v = grads4[i][0] * rx1 + grads4[i][1] * ry0 + grads4[i][2] * rz1 +
        grads4[i][3] * rt1;
    a = lerp(sx, u, v);
    i = tabindex4(ix, iy + 1, iz + 1, it + 1);
    u = grads4[i][0] * rx0 + grads4[i][1] * ry1 + grads4[i][2] * rz1 +
        grads4[i][3] * rt1;
    i = tabindex4(ix + 1, iy + 1, iz + 1, it + 1);
    v = grads4[i][0] * rx1 + grads4[i][1] * ry1 + grads4[i][2] * rz1 +
        grads4[i][3] * rt1;
    b = lerp(sx, u, v);
    d = lerp(sy, a, b);
    float f = lerp(sz, c, d);
    return lerp(st, e, f);
}

float Noise::snoise(float x, float y) const { return noise2d(x, y); }

float Noise::snoise(float x, float y, float z) const {
    return noise3d(x, y, z);
}

float Noise::snoise(float x, float y, float z, float t) const {
    return noise4d(x, y, z, t);
}

void Noise::vsnoise(float x, float y, float &ox, float &oy) const {
    ox = noise2d(x, y);
    oy = noise2d(x + 10.f, y);
}

void Noise::vsnoise(float x, float y, float z, float &ox, float &oy,
                    float &oz) const {
    ox = noise3d(x, y, z);
    oy = noise3d(x + 10.f, y, z);
    oz = noise3d(x + 10.f, y + 10.f, z);
}

void Noise::vsnoise(float x, float y, float z, float t, float &ox, float &oy,
                    float &oz, float &ot) const {
    ox = noise4d(x, y, z, t);
    oy = noise4d(x + 10.f, y, z, t);
    oz = noise4d(x + 10.f, y + 10.f, z, t);
    ot = noise4d(x + 10.f, y + 10.f, z + 10.f, t);
}

float Noise::fBm(float x, float y, float z, int octaves, float lacunarity,
                 float gain) const {
    float res = 0.f, amp = 1.f;
    for (int i = 0; i < octaves; ++i) {
        res += amp * noise3d(x, y, z);
        amp *= gain;
        x *= lacunarity;
        y *= lacunarity;
        z *= lacunarity;
    }
    return 0.5f * (res + 1.f);
}

float Noise::turbulence(float x, float y, float z, int octaves,
                        float lacunarity, float gain) const {
    float res = 0.f, amp = 1.f;
    for (int i = 0; i < octaves; ++i) {
        float n = noise3d(x, y, z);
        res += amp * (n < 0.f ? -n : n);
        amp *= gain;
        x *= lacunarity;
        y *= lacunarity;
        z *= lacunarity;
    }
    return 0.5f * (res + 1.f);
}

void Noise::vfBm(float x, float y, float z, int octaves, float lacunarity,
                 float gain, float &ox, float &oy, float &oz) const {
    ox = oy = oz = 0.f;
    float amp = 1.f;
    for (int i = 0; i < octaves; ++i) {
        float vx, vy, vz;
        vsnoise(x, y, z, vx, vy, vz);
        ox += amp * vx;
        oy += amp * vy;
        oz += amp * vz;
        amp *= gain;
        x *= lacunarity;
        y *= lacunarity;
        z *= lacunarity;
    }
}

void Noise::vturbulence(float x, float y, float z, int octaves,
                        float lacunarity, float gain, float &ox, float &oy,
                        float &oz) const {
    ox = oy = oz = 0.f;
    float amp = 1.f;
    for (int i = 0; i < octaves; ++i) {
        float vx, vy, vz;
        vsnoise(x, y, z, vx, vy, vz);
        ox += amp * (vx < 0.f ? -vx : vx);
        oy += amp * (vy < 0.f ? -vy : vy);
        oz += amp * (vz < 0.f ? -vz : vz);
        amp *= gain;
        x *= lacunarity;
        y *= lacunarity;
        z *= lacunarity;
    }
}

} // namespace Noise
} // namespace meshTools
