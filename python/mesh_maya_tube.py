import math
import meshTools.lists as lists
from meshTools.geometry import Transform, Vector
from meshTools.mesh import Point
import maya.OpenMaya as OpenMaya
from mesh_maya import MayaMesh


class TubeSegment:
    def __init__(self, **kwargs):
        self.parameter = kwargs.get("parameter", 0)
        self.angle = kwargs.get("angle", 0)
        self.origin = kwargs.get("origin")
        self.tangent = kwargs.get("tangent")
        self.normal = kwargs.get("normal")
        self.up = kwargs.get("up")
        self.length_param = kwargs.get("length", 0)
        self.first_knot = 0
        self.last_knot = 0

    def __getitem__(self, key):
        if key == 0:
            return self.origin
        if key == 1:
            return self.tangent
        if key == 2:
            return self.normal
        if key == 3:
            return self.up

    def __repr__(self):
        s = "param:" + str(self.parameter) + "\n"
        s += "length at parameter:" + str(self.length_param) + "\n"
        s += "origin:" + str(self.origin) + "\n"
        s += "tangent:" + str(self.tangent) + "\n"
        s += "normal:" + str(self.normal) + "\n"
        s += "up:" + str(self.up) + "\n"
        if self.first_knot and self.last_knot:
            s += "first:" + str(self.first_knot.parameter) + "\n"
            s += "last:" + str(self.last_knot.parameter) + "\n"
        return s


class MayaTube:
    def __init__(self, **kwargs):
        if "curveDag" in kwargs:
            curve_fn = OpenMaya.MFnNurbsCurve(kwargs.get("curveDag"))
        elif "curveFn" in kwargs:
            curve_fn = kwargs.get("curveFn")
        else:
            print("No input curve for MayaTube")
            return
        reverse = kwargs.get("reverse", 0)
        even = kwargs.get("even", 0)
        tile_scale = kwargs.get("scale", 1)
        taper = kwargs.get("taper", 0)
        twist = kwargs.get("twist", 0)
        tile_rotate = kwargs.get("rotate", 0)
        growth = kwargs.get("growth", 1)
        scale_corners = kwargs.get("scale_corners", 1)
        cylinder_segments = kwargs.get("cylinder_segments", 0)
        point = OpenMaya.MPoint()

        self.profile_closed = -1
        if cylinder_segments > 0:
            tile = MayaMesh(empty=1)
            combine_tile = MayaMesh(empty=1)
            tile.faces = [[]]
            for i in range(cylinder_segments):
                tile.vertices += [
                    Point(
                        math.sin(
                            2
                            * math.pi
                            / cylinder_segments
                            * (cylinder_segments - i + 1)
                        )
                        * tile_scale,
                        0,
                        math.cos(
                            2
                            * math.pi
                            / cylinder_segments
                            * (cylinder_segments - i + 1)
                        )
                        * tile_scale,
                    )
                ]
                tile.faces[0] += [i]
            tile.vertices = tile.vertices[::-1]
        elif "profileDag" in kwargs:
            profileDag = kwargs.get("profileDag")
            if profileDag.hasFn(OpenMaya.MFn.kMesh):
                tile = MayaMesh(dag=profileDag, vertices=1, faces=1)
            elif profileDag.hasFn(OpenMaya.MFn.kNurbsCurve):
                profile_curve_fn = OpenMaya.MFnNurbsCurve(profileDag)
                self.profile_closed = not (
                    profile_curve_fn.form() == OpenMaya.MFnNurbsCurve.kOpen
                )
                tile = MayaMesh(empty=1)
                l = []
                for i in range(profile_curve_fn.numCVs()):
                    l += [profile_curve_fn.knot(i)]
                l = lists.group_duplicates(l)
                tile.faces = [[]]
                for i in range(len(l) - self.profile_closed):
                    try:
                        profile_curve_fn.getPointAtParam(
                            l[i], point, OpenMaya.MSpace.kWorld
                        )
                        tile.vertices += [Point(point)]
                        tile.faces[0] += [len(tile.vertices) - 1]

                    except Exception as e:
                        print("except profileDag,%s" % e)
            else:
                print("Unknown class of input profile")
                return
            combine_tile = MayaMesh(empty=1)

        elif "profileFn" in kwargs:
            profileFn = kwargs.get("profileFn")
            if profileFn.type() == 295:  # "kMesh"
                tile = MayaMesh(mesh=profileFn, vertices=1, faces=1)
            elif profileFn.type() == 266:  # "kNurbsCurve"
                profile_curve_fn = profileFn
                self.profile_closed = not (
                    profile_curve_fn.form() == OpenMaya.MFnNurbsCurve.kOpen
                )
                tile = MayaMesh(empty=1)
                l = []
                for i in range(profile_curve_fn.numCVs()):
                    l += [profile_curve_fn.knot(i)]
                l = lists.group_duplicates(l)
                tile.faces = [[]]
                for i in range(len(l) - self.profile_closed):
                    try:
                        profile_curve_fn.getPointAtParam(
                            l[i], point, OpenMaya.MSpace.kWorld
                        )
                        tile.vertices += [Point(point)]
                        tile.faces[0] += [len(tile.vertices) - 1]
                    except Exception as e:
                        print("except profileFn,%s" % e)
            combine_tile = MayaMesh(empty=1)
        else:
            print("No input profile for MayaTube")
            return

        l = []
        for i in range(curve_fn.numCVs()):
            l += [curve_fn.knot(i)]
        l = lists.group_duplicates(l)
        nsegments = kwargs.get("segments", 5)
        fix = kwargs.get("fix", 0)
        t_translate = Transform()
        t_rotate = Transform()
        t_scale = Transform()
        t_final = Transform()

        self.tube_segments = []
        self.knots = []
        self.closed = curve_fn.form() == 3

        if reverse == 1:
            l = l[::-1]
            tile.vertices = tile.vertices[::-1]
        if even == 0:
            # in case of param distribution
            self.curve_length = 0
            for i in range(len(l)):
                try:
                    print(l[i], point)
                    curve_fn.getPointAtParam(
                        l[i], point, OpenMaya.MSpace.kWorld
                    )
                    self.knots += [
                        TubeSegment(
                            parameter=l[i],
                            origin=Vector(point.x, point.y, point.z),
                        )
                    ]
                except Exception as e:
                    print("except knots,%s" % e)
            for i in range(len(self.knots)):
                for j in range(nsegments):
                    if i == len(self.knots) - 1 and j > 0:
                        continue
                    if i == len(self.knots) - 1:
                        param = self.knots[-1].parameter
                    else:
                        param = (
                            self.knots[i].parameter
                            + (
                                self.knots[i + 1].parameter
                                - self.knots[i].parameter
                            )
                            / float(nsegments)
                            * j
                        )
                    if param == self.knots[i].parameter:
                        self.tube_segments += [self.knots[i]]
                        if param != self.knots[0].parameter:
                            length = (
                                self.tube_segments[-1].origin
                                - self.tube_segments[-2].origin
                            ).length()
                            self.tube_segments[-1].length_param = (
                                self.tube_segments[-2].length_param + length
                            )
                            self.curve_length += length
                            self.knots[i].first_knot = self.knots[i - 1]
                        if param != self.knots[-1].parameter:
                            self.knots[i].last_knot = self.knots[i + 1]
                    else:
                        try:
                            curve_fn.getPointAtParam(
                                param, point, OpenMaya.MSpace.kWorld
                            )
                            try:
                                curve_fn.normal(
                                    param, OpenMaya.MSpace.kWorld
                                )
                            except Exception:
                                if param != self.knots[i].parameter:
                                    continue
                            self.tube_segments += [
                                TubeSegment(
                                    parameter=param,
                                    origin=Vector(point.x, point.y, point.z),
                                )
                            ]
                            self.tube_segments[-1].first_knot = self.knots[i]
                            self.tube_segments[-1].last_knot = self.knots[i + 1]
                            length = (
                                self.tube_segments[-1].origin
                                - self.tube_segments[-2].origin
                            ).length()
                            self.tube_segments[-1].length_param = (
                                self.tube_segments[-2].length_param + length
                            )
                            self.curve_length += length
                        except Exception as e:
                            print("except length,%s" % e)
            self.curve_length *= growth
        else:
            # in case of even distribution
            self.curve_length = curve_fn.length()
            for i in range(len(l)):
                try:
                    curve_fn.getPointAtParam(
                        l[i], point, OpenMaya.MSpace.kWorld
                    )
                    self.knots += [
                        TubeSegment(
                            parameter=l[i],
                            origin=Vector(point.x, point.y, point.z),
                        )
                    ]
                    if i > 0:
                        self.knots[-1].length_param = self.knots[
                            -2
                        ].length_param + self.measureSegment(
                            curve_fn, l[i - 1], l[i], 100
                        )
                except Exception as e:
                    print("except knots even,%s" % e)

            first_knot = 0
            self.curve_length *= growth
            for i in range(nsegments):
                param = curve_fn.findParamFromLength(
                    i * self.curve_length / float(nsegments - 1)
                )
                try:
                    curve_fn.getPointAtParam(
                        param, point, OpenMaya.MSpace.kWorld
                    )
                    self.tube_segments += [
                        TubeSegment(
                            parameter=param,
                            origin=Vector(point.x, point.y, point.z),
                        )
                    ]
                    if len(self.tube_segments) < 2:
                        continue
                    length = (
                        self.tube_segments[-1].origin
                        - self.tube_segments[-2].origin
                    ).length()
                    self.tube_segments[-1].length_param = (
                        self.tube_segments[-2].length_param + length
                    )
                    if self.tube_segments[-1].length_param > self.knots[
                        first_knot + 1
                    ].length_param and first_knot <= len(self.knots):
                        first_knot += 1
                    self.tube_segments[-1].first_knot = self.knots[first_knot]
                    self.tube_segments[-1].last_knot = self.knots[
                        first_knot + 1
                    ]
                except Exception as e:
                    print("except first last knot,%s" % e)

        y_axis = Vector(0, 1, 0)
        z_axis = Vector(0, 0, 1)
        tile_vert_count = len(tile.vertices)
        tile_face_count = len(tile.faces)
        tile_vf = tile_vert_count + tile_face_count

        self.segments_count = len(self.tube_segments)

        # Case of 2-point curve
        if len(self.knots) == 2:
            self.knots[0].tangent = (
                self.knots[0].origin - self.knots[1].origin
            ).normalize()
            self.knots[1].tangent = self.knots[0].tangent
            self.knots[0].normal = y_axis.cross(
                self.knots[0].tangent
            ).normalize()
            if self.knots[0].normal.isNull():
                self.knots[0].normal = z_axis.cross(
                    self.knots[0].tangent
                ).normalize()
            self.knots[1].normal = self.knots[0].normal
        else:
            # Precalculate axis
            for i in range(len(self.knots)):
                seg = self.knots[i]

                if i == 0:
                    a = (
                        self.knots[i + 2].origin - self.knots[i + 1].origin
                    ).normalize()
                    b = (seg.origin - self.knots[i + 1].origin).normalize()
                    seg.tangent = (
                        self.knots[i + 1].origin - seg.origin
                    ).normalize()
                    seg.normal = a.cross(b).normalize()
                    if seg.normal.isNull():
                        seg.normal = y_axis.cross(seg.tangent).normalize()
                    if seg.normal.isNull():
                        seg.normal = z_axis.cross(seg.tangent).normalize()
                elif i == len(self.knots) - 1:
                    seg.tangent = (
                        seg.origin - self.knots[i - 1].origin
                    ).normalize()
                    seg.normal = self.knots[i - 1].normal
                else:
                    a = (self.knots[i + 1].origin - seg.origin).normalize()
                    b = (self.knots[i - 1].origin - seg.origin).normalize()
                    seg.angle = a.angle(b)
                    seg.tangent = (a - b).normalize()
                    seg.normal = a.cross(b).normalize()
                    if seg.normal.isNull():
                        seg.normal = self.knots[i - 1].normal
                    dot = seg.normal.dot(self.knots[i - 1].normal)
                    if dot < 0:
                        seg.normal = -1 * seg.normal

        # fill segment lengths
        segment_lengths = [0]
        # total_length=0
        profile_length = 0
        for i in range(1, len(tile.vertices)):
            profile_length += (tile.vertices[i] - tile.vertices[i - 1]).length()
        for i in range(1, self.segments_count):
            segment_lengths += [
                segment_lengths[-1]
                + (
                    self.tube_segments[i].origin
                    - self.tube_segments[i - 1].origin
                ).length()
            ]
        for i in range(len(segment_lengths)):
            segment_lengths[i] = segment_lengths[i] / profile_length

        for i in range(self.segments_count):
            seg = self.tube_segments[i]
            if even == 0 and seg.length_param > self.curve_length:
                continue

            if self.segments_count > 2:
                if i == 0:
                    a = (
                        self.tube_segments[i + 2].origin
                        - self.tube_segments[i + 1].origin
                    ).normalize()
                    b = (
                        self.tube_segments[i].origin
                        - self.tube_segments[i + 1].origin
                    ).normalize()
                    seg.tangent = (
                        self.tube_segments[i + 1].origin - seg.origin
                    ).normalize()
                    seg.normal = a.cross(b).normalize()
                elif i == self.segments_count - 1:
                    seg.tangent = (
                        seg.origin - self.tube_segments[i - 1].origin
                    ).normalize()
                    seg.normal = self.tube_segments[i - 1].normal
                else:
                    a = (
                        self.tube_segments[i + 1].origin - seg.origin
                    ).normalize()
                    b = (
                        self.tube_segments[i - 1].origin - seg.origin
                    ).normalize()
                    seg.angle = a.angle(b)
                    seg.tangent = (a - b).normalize()
                    if math.modf(seg.parameter / 1.0)[0] > 0:
                        if fix == 0:
                            seg.normal = seg.first_knot.normal.lerp(
                                seg.last_knot.normal,
                                (seg.length_param - seg.first_knot.length_param)
                                / float(
                                    seg.last_knot.length_param
                                    - seg.first_knot.length_param
                                ),
                            ).normalize()
                        else:
                            seg.normal = seg.first_knot.normal.slerp(
                                seg.last_knot.normal,
                                (seg.length_param - seg.first_knot.length_param)
                                / float(
                                    seg.last_knot.length_param
                                    - seg.first_knot.length_param
                                ),
                            ).normalize()

                    if (
                        fix == 1
                        and abs(
                            seg.normal.dot(self.tube_segments[i - 1].normal)
                        )
                        < 0.9
                    ):
                        seg.normal = self.tube_segments[i - 1].normal
                    elif (
                        fix == 2
                        and abs(
                            seg.normal.dot(self.tube_segments[i - 1].normal)
                        )
                        < 0.9
                    ):
                        seg.normal = seg.normal.lerp(
                            self.tube_segments[i - 1].normal, 0.5
                        )
                    elif fix == 3:
                        seg.normal = y_axis
            t_translate = t_translate.lookAt(
                seg.origin, seg.origin + seg.normal, seg.tangent
            )
            # Apply transforms

            t_final = t_translate

            if scale_corners and i > 0 and i < self.segments_count - 1:
                if (
                    math.modf(seg.angle / (math.pi / 2.0))[0] > 0.01
                    and math.modf(seg.angle / (math.pi / 2.0))[0] < 0.99
                ):
                    t_scale = t_scale.scale(
                        Vector(abs(1 / math.sin(seg.angle / 2)), 1, 1)
                    )
                    t_final = t_translate * t_scale
            if self.curve_length == 0.0:
                taper_value = 0.0
            else:
                taper_value = (
                    tile_scale * taper * seg.length_param / self.curve_length
                )
            if taper_value == tile_scale:
                taper_value = tile_scale * 0.999
            t_scale = t_scale.scale(
                Vector(tile_scale - taper_value, 1, tile_scale - taper_value)
            )
            t_final *= t_scale

            twist_value = twist * seg.length_param / self.curve_length
            t_rotate = t_rotate.rotateY(math.radians(tile_rotate + twist_value))
            t_final *= t_rotate

            combine_tile.multiDuplicateTransform(tile, t_final, faces=0)
            # Generate UVs

            for k in range(tile_face_count):
                vert_count = len(tile.faces[k])
                for j in range(vert_count + 1):
                    combine_tile.uvs += [
                        Vector(
                            1 - j / float(vert_count) + k + k * 0.01,
                            segment_lengths[i],
                            0,
                        )
                    ]
            # Build mesh
            if i == 0:
                continue
            cvert_count = 0
            for k in range(tile_face_count):
                vert_count = len(tile.faces[k])

                for j in range(
                    vert_count
                    - (cylinder_segments == 2)
                    - (self.profile_closed == 0)
                ):
                    if j < vert_count - 1:
                        a = tile.faces[k][j]
                        b = tile.faces[k][j + 1]
                    else:
                        a = tile.faces[k][j]
                        b = tile.faces[k][0]
                    jcvert = j + cvert_count + i * tile_vf
                    combine_tile.face_uvs += [
                        [
                            jcvert - tile_vf + 1,
                            jcvert - tile_vf,
                            jcvert,
                            1 + jcvert,
                        ]
                    ][::-1]
                    if (
                        self.closed
                        and i == self.segments_count - 1
                        and growth == 1
                    ):
                        combine_tile.faces += [
                            [
                                (i - 1) * tile_vert_count + b,
                                (i - 1) * tile_vert_count + a,
                                a,
                                b,
                            ]
                        ][::-1]
                    else:
                        combine_tile.faces += [
                            [
                                (i - 1) * tile_vert_count + b,
                                (i - 1) * tile_vert_count + a,
                                i * tile_vert_count + a,
                                i * tile_vert_count + b,
                            ]
                        ][::-1]

                cvert_count += vert_count + 1
        if kwargs.get("cap", 0) and not self.closed:
            end_caps = []
            for i in range(len(tile.faces)):
                end_caps += [
                    lists.offset(
                        tile.faces[i],
                        (self.segments_count - 1) * tile_vert_count,
                    )[::-1]
                ]
            combine_tile.faces += tile.faces + end_caps
            combine_tile.face_uvs += tile.faces + tile.faces

        if "parent" in kwargs:
            combine_tile.meshToMaya(uvs=1, parent=kwargs.get("parent"))
        else:
            combine_tile.meshToMaya(uvs=1)

    def measureSegment(self, curve_fn, start, end, steps):
        pRange = end - start
        step = pRange / float(steps)
        length = 0
        p1 = OpenMaya.MPoint()
        p2 = OpenMaya.MPoint()
        for i in range(steps - 1):
            curve_fn.getPointAtParam(start + i * step, p1)
            curve_fn.getPointAtParam(start + (i + 1) * step, p2)
            length += p1.distanceTo(p2)
        return length
