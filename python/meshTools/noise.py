"""Simplex-style procedural noise for 2D, 3D, and 4D coordinates.

Provides scalar and vector variants: snoise, vsnoise, fBm, turbulence, etc.
All noise returns values in [-1, 1] unless noted. Uses gradient tables from
noise_tabs for deterministic, repeatable results. Uses C++ _noise extension
when available.
"""

from math import floor

from .noise_tabs import grads2, grads3, grads4, perm

TABMASK = 0xFF

try:
    from . import _noise
    _NoiseCpp = _noise.Noise
except ImportError:
    try:
        import _noise
        _NoiseCpp = _noise.Noise
    except ImportError:
        _NoiseCpp = None


def floor2int(val: float) -> int:
    """Convert float to int via floor.

    Args:
        val: Input value.

    Returns:
        Floored integer.
    """
    return int(floor(val))


def lerp(t: float, a: float, b: float) -> float:
    """Linear interpolation: a + (b - a) * t.

    Args:
        t: Interpolation parameter in [0, 1].
        a: Start value.
        b: End value.

    Returns:
        Interpolated value.
    """
    return a + (b - a) * t


def clamp(val: float, low: float, high: float) -> float:
    """Clamp val to [low, high].

    Args:
        val: Value to clamp.
        low: Lower bound.
        high: Upper bound.

    Returns:
        Clamped value in [low, high].
    """
    if val < low:
        return low
    elif val > high:
        return high
    else:
        return val


def imod(a: float, b: float) -> float:
    """Integer modulo: remainder of a / b, always in [0, b).

    Args:
        a: Dividend.
        b: Divisor.

    Returns:
        Remainder in [0, b).
    """
    n = int(a / float(b))
    a -= n * b
    if a < 0:
        a += b
    return a


class NoisePy(object):
    """Procedural Simplex-style noise generator (pure Python implementation)."""

    def __init__(self):
        self.xperiod = 1
        self.yperiod = 1
        self.zperiod = 1
        self.tperiod = 1
        self.poffset = 0

    def noise_template(self, func, *args):
        """
        noise template (2D)

        Noise template for a 2D noise or pnoise function.
        The template parameter specifies the function that's used to create
        an index for the random values. If this function is periodic you'll
        also get a periodic noise.
        Returns a value between -1 and 1
        """
        if len(args) == 2:
            x, y = args[0], args[1]
            ix, iy = floor2int(x), floor2int(y)
            rx0 = x - ix
            ry0 = y - iy
            rx1 = rx0 - 1
            ry1 = ry0 - 1
            sx = rx0 * rx0 * (3 - 2 * rx0)
            sy = ry0 * ry0 * (3 - 2 * ry0)

            g = grads2[func(ix, iy)]
            u = g[0] * rx0 + g[1] * ry0
            g = grads2[func(ix + 1, iy)]
            v = g[0] * rx1 + g[1] * ry0
            a = lerp(sx, u, v)

            g = grads2[func(ix, iy + 1)]
            u = g[0] * rx0 + g[1] * ry1
            g = grads2[func(ix + 1, iy + 1)]
            v = g[0] * rx1 + g[1] * ry1
            b = lerp(sx, u, v)

            return lerp(sy, a, b)
        """
        noise template (3D)

        Noise template for a 3D noise or pnoise function.
        The template parameter specifies the function that's used to create
        an index for the random values. If this function is periodic you'll
        also get a periodic noise.
        Returns a value between -1 and 1 
        """
        if len(args) == 3:
            x, y, z = args[0], args[1], args[2]
            ix, iy, iz = floor2int(x), floor2int(y), floor2int(z)
            rx0 = x - ix
            ry0 = y - iy
            rz0 = z - iz
            rx1 = rx0 - 1
            ry1 = ry0 - 1
            rz1 = rz0 - 1
            sx = rx0 * rx0 * (3 - 2 * rx0)
            sy = ry0 * ry0 * (3 - 2 * ry0)
            sz = rz0 * rz0 * (3 - 2 * rz0)

            g = grads3[func(ix, iy, iz)]
            u = g[0] * rx0 + g[1] * ry0 + g[2] * rz0
            g = grads3[func(ix + 1, iy, iz)]
            v = g[0] * rx1 + g[1] * ry0 + g[2] * rz0
            a = lerp(sx, u, v)

            g = grads3[func(ix, iy + 1, iz)]
            u = g[0] * rx0 + g[1] * ry1 + g[2] * rz0
            g = grads3[func(ix + 1, iy + 1, iz)]
            v = g[0] * rx1 + g[1] * ry1 + g[2] * rz0
            b = lerp(sx, u, v)

            c = lerp(sy, a, b)

            g = grads3[func(ix, iy, iz + 1)]
            u = g[0] * rx0 + g[1] * ry0 + g[2] * rz1
            g = grads3[func(ix + 1, iy, iz + 1)]
            v = g[0] * rx1 + g[1] * ry0 + g[2] * rz1
            a = lerp(sx, u, v)

            g = grads3[func(ix, iy + 1, iz + 1)]
            u = g[0] * rx0 + g[1] * ry1 + g[2] * rz1
            g = grads3[func(ix + 1, iy + 1, iz + 1)]
            v = g[0] * rx1 + g[1] * ry1 + g[2] * rz1
            b = lerp(sx, u, v)

            d = lerp(sy, a, b)

            return lerp(sz, c, d)
        """
        noise template (3D)

        Noise template for a 3D noise or pnoise function.
        The template parameter specifies the function that's used to create
        an index for the random values. If this function is periodic you'll
        also get a periodic noise.
        Returns a value between -1 and 1 
        """
        if len(args) == 4:
            x, y, z, t = args[0], args[1], args[2], args[3]
            ix, iy, iz, it = (
                floor2int(x),
                floor2int(y),
                floor2int(z),
                floor2int(t),
            )
            rx0 = x - ix
            ry0 = y - iy
            rz0 = z - iz
            rt0 = t - it
            rx1 = rx0 - 1
            ry1 = ry0 - 1
            rz1 = rz0 - 1
            rt1 = rt0 - 1
            sx = rx0 * rx0 * (3 - 2 * rx0)
            sy = ry0 * ry0 * (3 - 2 * ry0)
            sz = rz0 * rz0 * (3 - 2 * rz0)
            st = rt0 * rt0 * (3 - 2 * rt0)
            g = grads4[func(ix, iy, iz, it)]
            u = g[0] * rx0 + g[1] * ry0 + g[2] * rz0 + g[3] * rt0
            g = grads4[func(ix + 1, iy, iz, it)]
            v = g[0] * rx1 + g[1] * ry0 + g[2] * rz0 + g[3] * rt0
            a = lerp(sx, u, v)

            g = grads4[func(ix, iy + 1, iz, it)]
            u = g[0] * rx0 + g[1] * ry1 + g[2] * rz0 + g[3] * rt0
            g = grads4[func(ix + 1, iy + 1, iz, it)]
            v = g[0] * rx1 + g[1] * ry1 + g[2] * rz0 + g[3] * rt0
            b = lerp(sx, u, v)

            c = lerp(sy, a, b)

            g = grads4[func(ix, iy, iz + 1, it)]
            u = g[0] * rx0 + g[1] * ry0 + g[2] * rz1 + g[3] * rt0
            g = grads4[func(ix + 1, iy, iz + 1, it)]
            v = g[0] * rx1 + g[1] * ry0 + g[2] * rz1 + g[3] * rt0
            a = lerp(sx, u, v)

            g = grads4[func(ix, iy + 1, iz + 1, it)]
            u = g[0] * rx0 + g[1] * ry1 + g[2] * rz1 + g[3] * rt0
            g = grads4[func(ix + 1, iy + 1, iz + 1, it)]
            v = g[0] * rx1 + g[1] * ry1 + g[2] * rz1 + g[3] * rt0
            b = lerp(sx, u, v)

            d = lerp(sy, a, b)

            e = lerp(sz, c, d)

            g = grads4[func(ix, iy, iz, it + 1)]
            u = g[0] * rx0 + g[1] * ry0 + g[2] * rz0 + g[3] * rt1
            g = grads4[func(ix + 1, iy, iz, it + 1)]
            v = g[0] * rx1 + g[1] * ry0 + g[2] * rz0 + g[3] * rt1
            a = lerp(sx, u, v)

            g = grads4[func(ix, iy + 1, iz, it + 1)]
            u = g[0] * rx0 + g[1] * ry1 + g[2] * rz0 + g[3] * rt1
            g = grads4[func(ix + 1, iy + 1, iz, it + 1)]
            v = g[0] * rx1 + g[1] * ry1 + g[2] * rz0 + g[3] * rt1
            b = lerp(sx, u, v)

            c = lerp(sy, a, b)

            g = grads4[func(ix, iy, iz + 1, it + 1)]
            u = g[0] * rx0 + g[1] * ry0 + g[2] * rz1 + g[3] * rt1
            g = grads4[func(ix + 1, iy, iz + 1, it + 1)]
            v = g[0] * rx1 + g[1] * ry0 + g[2] * rz1 + g[3] * rt1
            a = lerp(sx, u, v)

            g = grads4[func(ix, iy + 1, iz + 1, it + 1)]
            u = g[0] * rx0 + g[1] * ry1 + g[2] * rz1 + g[3] * rt1
            g = grads4[func(ix + 1, iy + 1, iz + 1, it + 1)]
            v = g[0] * rx1 + g[1] * ry1 + g[2] * rz1 + g[3] * rt1
            b = lerp(sx, u, v)

            d = lerp(sy, a, b)

            f = lerp(sz, c, d)

            return lerp(st, e, f)

    def tabindex2(self, ix: int, iy: int) -> int:
        """Hash (ix, iy) to permutation index for 2D noise.

        Args:
            ix: Integer x coordinate.
            iy: Integer y coordinate.

        Returns:
            Permutation table index.
        """
        return perm[(ix + perm[iy & TABMASK]) & TABMASK]

    def tabindex3(self, ix: int, iy: int, iz: int) -> int:
        """Hash (ix, iy, iz) to permutation index for 3D noise.

        Args:
            ix: Integer x coordinate.
            iy: Integer y coordinate.
            iz: Integer z coordinate.

        Returns:
            Permutation table index.
        """
        return perm[(ix + perm[(iy + perm[iz & TABMASK]) & TABMASK]) & TABMASK]

    def tabindex4(self, ix: int, iy: int, iz: int, it: int) -> int:
        """Hash (ix, iy, iz, it) to permutation index for 4D noise.

        Args:
            ix: Integer x coordinate.
            iy: Integer y coordinate.
            iz: Integer z coordinate.
            it: Integer t coordinate.

        Returns:
            Permutation table index.
        """
        return perm[
            (
                it
                + perm[
                    (ix + perm[(iy + perm[iz & TABMASK]) & TABMASK]) & TABMASK
                ]
            )
            & TABMASK
        ]

    def snoise(self, *args) -> float:
        """Scalar noise. Accepts (x,y), (x,y,z), (x,y,z,t), or Vector.

        Returns:
            Noise value in [-1, 1].
        """
        if len(args) == 1:
            x, y, z = args[0].x, args[0].y, args[0].z
            return self.noise_template(self.tabindex3, x, y, z)
        if len(args) == 2:
            x, y = args[0], args[1]
            return self.noise_template(self.tabindex2, x, y)
        if len(args) == 3:
            x, y, z = args[0], args[1], args[2]
            return self.noise_template(self.tabindex3, x, y, z)
        if len(args) == 4:
            x, y, z, t = args[0], args[1], args[2], args[3]
            return self.noise_template(self.tabindex4, x, y, z, t)

    def fBm(
        self,
        x: float,
        y: float,
        z: float,
        octaves: int,
        lacunarity: float,
        gain: float,
    ) -> float:
        """Fractional Brownian motion: summed octaves of scaled snoise.

        Args:
            x, y, z: 3D coordinates.
            octaves: Number of noise octaves.
            lacunarity: Frequency multiplier per octave.
            gain: Amplitude multiplier per octave.

        Returns:
            fBm value in [0, 1].
        """
        res = 0
        amp = 1
        for i in range(octaves):
            res += amp * self.snoise(x, y, z)
            amp *= gain
            x *= lacunarity
            y *= lacunarity
            z *= lacunarity
        return 0.5 * (res + 1.0)

    def vfBm(
        self,
        x: float,
        y: float,
        z: float,
        octaves: int,
        lacunarity: float,
        gain: float,
    ) -> list[float]:
        """Vector fBm: summed vector noise octaves.

        Args:
            x, y, z: 3D coordinates.
            octaves: Number of noise octaves.
            lacunarity: Frequency multiplier per octave.
            gain: Amplitude multiplier per octave.

        Returns:
            [ox, oy, oz] vector components.
        """
        amp = 1
        ox, oy, oz = 0.0, 0.0, 0.0

        for i in range(octaves):
            v = self.vsnoise(x, y, z)
            ox += amp * v[0]
            oy += amp * v[1]
            oz += amp * v[2]
            amp *= gain
            x *= lacunarity
            y *= lacunarity
            z *= lacunarity
        # ox = 0.5*(ox+1.0)
        # oy = 0.5*(oy+1.0)
        # oz = 0.5*(oz+1.0)
        return [ox, oy, oz]

    def turbulence(
        self,
        x: float,
        y: float,
        z: float,
        octaves: int,
        lacunarity: float,
        gain: float,
    ) -> float:
        """Turbulence: fBm using absolute noise values.

        Args:
            x, y, z: 3D coordinates.
            octaves: Number of noise octaves.
            lacunarity: Frequency multiplier per octave.
            gain: Amplitude multiplier per octave.

        Returns:
            Turbulence value in [0, 1].
        """
        res = 0
        amp = 1
        for i in range(octaves):
            res += amp * abs(self.snoise(x, y, z))
            amp *= gain
            x *= lacunarity
            y *= lacunarity
            z *= lacunarity
        return 0.5 * (res + 1.0)

    def vturbulence(
        self,
        x: float,
        y: float,
        z: float,
        octaves: int,
        lacunarity: float,
        gain: float,
    ) -> list[float]:
        """Vector turbulence: summed abs(vsnoise) octaves.

        Args:
            x, y, z: 3D coordinates.
            octaves: Number of noise octaves.
            lacunarity: Frequency multiplier per octave.
            gain: Amplitude multiplier per octave.

        Returns:
            [ox, oy, oz] vector components.
        """
        amp = 1.0
        ox = 0.0
        oy = 0.0
        oz = 0.0
        for i in range(octaves):
            v = self.vsnoise(x, y, z)
            ox += amp * abs(v[0])
            oy += amp * abs(v[1])
            oz += amp * abs(v[2])
            amp *= gain
            x *= lacunarity
            y *= lacunarity
            z *= lacunarity
        # ox = 0.5*(ox+1.0)
        # oy = 0.5*(oy+1.0)
        # oz = 0.5*(oz+1.0)
        return [ox, oy, oz]

    def vsnoise(self, *args: float) -> list[float] | tuple[float, float]:
        """Vector noise.

        Args:
            *args: (x,y), (x,y,z), (x,y,z,t), or single Vector.

        Returns:
            [ox, oy] (2D), [ox, oy, oz] (3D), or [ox, oy, oz, ot] (4D).
        """
        if len(args) == 1:
            x, y, z = args[0].x, args[0].y, args[0].z
            ox = self.noise_template(self.tabindex3, x, y, z)
            x += 10
            oy = self.noise_template(self.tabindex3, x, y, z)
            y += 10
            oz = self.noise_template(self.tabindex3, x, y, z)
            return [ox, oy, oz]
        if len(args) == 2:
            x, y = args[0], args[1]
            ox = self.noise_template(self.tabindex2, x, y)
            x += 10
            oy = self.noise_template(self.tabindex2, x, y)
            return ox, oy
        if len(args) == 3:
            x, y, z = args[0], args[1], args[2]
            ox = self.noise_template(self.tabindex3, x, y, z)
            x += 10
            oy = self.noise_template(self.tabindex3, x, y, z)
            y += 10
            oz = self.noise_template(self.tabindex3, x, y, z)
            return [ox, oy, oz]
        if len(args) == 4:
            x, y, z, t = args[0], args[1], args[2], args[3]
            ox = self.noise_template(self.tabindex4, x, y, z, t)
            x += 10
            oy = self.noise_template(self.tabindex4, x, y, z, t)
            y += 10
            oz = self.noise_template(self.tabindex4, x, y, z, t)
            z += 10
            ot = self.noise_template(self.tabindex4, x, y, z, t)
            return [ox, oy, oz, ot]


def _make_noise_class():
    """Return Noise class: C++ wrapper if available, else pure Python."""
    if _NoiseCpp is None:
        return NoisePy

    class Noise(object):
        """Procedural Simplex-style noise generator (uses C++ when available)."""

        def __init__(self):
            self._impl = _NoiseCpp()
            self.xperiod = 1
            self.yperiod = 1
            self.zperiod = 1
            self.tperiod = 1
            self.poffset = 0

        def snoise(self, *args):
            if len(args) == 1:
                v = args[0]
                return self._impl.snoise(v.x, v.y, v.z)
            if len(args) == 2:
                return self._impl.snoise(args[0], args[1])
            if len(args) == 3:
                return self._impl.snoise(args[0], args[1], args[2])
            if len(args) == 4:
                return self._impl.snoise(args[0], args[1], args[2], args[3])
            raise TypeError("snoise takes 1, 2, 3, or 4 arguments")

        def vsnoise(self, *args):
            if len(args) == 1:
                v = args[0]
                return list(self._impl.vsnoise(v.x, v.y, v.z))
            if len(args) == 2:
                return list(self._impl.vsnoise(args[0], args[1]))
            if len(args) == 3:
                return list(self._impl.vsnoise(args[0], args[1], args[2]))
            if len(args) == 4:
                return list(self._impl.vsnoise(args[0], args[1], args[2], args[3]))
            raise TypeError("vsnoise takes 1, 2, 3, or 4 arguments")

        def fBm(self, x, y, z, octaves, lacunarity, gain):
            return self._impl.fBm(x, y, z, octaves, lacunarity, gain)

        def turbulence(self, x, y, z, octaves, lacunarity, gain):
            return self._impl.turbulence(x, y, z, octaves, lacunarity, gain)

        def vfBm(self, x, y, z, octaves, lacunarity, gain):
            return list(self._impl.vfBm(x, y, z, octaves, lacunarity, gain))

        def vturbulence(self, x, y, z, octaves, lacunarity, gain):
            return list(self._impl.vturbulence(x, y, z, octaves, lacunarity, gain))

    return Noise


Noise = _make_noise_class()
