/**
 * @file mesh.h
 * @brief Mesh data structure with vertices, edges, and faces
 */

#pragma once

#include <geometry/bbox.h>
#include <geometry/vector.h>
#include <vector>

namespace meshTools {

/**
 * @namespace meshTools::Mesh
 * @brief Mesh data structures and operations
 */
namespace Mesh {

using namespace Geometry;

class Edge;
class Face;

/**
 * @class Vert
 * @brief Mesh vertex class
 *
 * Represents a vertex in a mesh with position and connectivity information.
 */
class Vert {
  public:
    /** @brief Default constructor */
    Vert() {}

    unsigned int id;           ///< Vertex ID
    Vector v;                  ///< Vertex position
    std::vector<Edge *> edges; ///< Connected edges
    std::vector<Face *> faces; ///< Connected faces

    /**
     * @brief Compute dot product with another vertex's position
     * @param other The other vertex
     * @return Dot product result
     */
    float dot(const Vert &other) const;

    /**
     * @brief Compute cross product with another vertex's position
     * @param other The other vertex
     * @return Cross product result
     */
    Vector cross(const Vert &other) const;

    /**
     * @brief Get all neighboring vertices
     * @return Vector of neighboring vertex pointers
     */
    std::vector<Vert *> neighbors() const;

    /**
     * @brief Compute the vertex normal based on connected faces
     * @return Computed normal vector
     */
    Vector computeNormal() const;
};

/**
 * @class Edge
 * @brief Mesh edge class
 *
 * Represents an edge in a mesh connecting two vertices.
 */
class Edge {
  public:
    /** @brief Default constructor */
    Edge() {}

    unsigned int id;           ///< Edge ID
    Vert *verts[2];            ///< Two vertices forming the edge
    std::vector<Face *> faces; ///< Connected faces

    /**
     * @brief Compute the edge normal based on connected faces
     * @return Computed normal vector
     */
    Vector computeNormal() const;

    /**
     * @brief Array subscript operator for non-const access
     * @param index Vertex index (0 or 1)
     * @return Pointer to the vertex at the specified index
     */
    Vert *operator[](const size_t &index) { return verts[index]; }

    /**
     * @brief Array subscript operator for const access
     * @param index Vertex index (0 or 1)
     * @return Pointer to the vertex at the specified index
     */
    Vert *operator[](const size_t &index) const { return verts[index]; }
};

/**
 * @class Face
 * @brief Mesh face (polygon) class
 *
 * Represents a face in a mesh, typically a triangle or polygon.
 */
class Face {
  public:
    /** @brief Default constructor */
    Face() {}

    unsigned int id;           ///< Face ID
    std::vector<Vert *> verts; ///< Vertices forming the face
    std::vector<Edge *> edges; ///< Edges forming the face
    Vector normal;             ///< Face normal vector

    /**
     * @brief Convert face vertices to pairs
     * @return Vector of vertex pairs
     */
    std::vector<Vert *> toPairs() const;

    /**
     * @brief Check if a point is inside the face
     * @param v The point to test
     * @return True if point is inside the face, false otherwise
     */
    bool isPointInside(const Vector &v) const;

    /**
     * @brief Compute the face normal from vertices
     * @return Computed normal vector
     */
    Vector computeNormal() const;

    /**
     * @brief Compute the center point of the face
     * @return Center point vector
     */
    Vector computeCenter() const;

    /**
     * @brief Array subscript operator for non-const access
     * @param index Vertex index
     * @return Pointer to the vertex at the specified index
     */
    Vert *operator[](const size_t &index) { return verts[index]; }

    /**
     * @brief Array subscript operator for const access
     * @param index Vertex index
     * @return Pointer to the vertex at the specified index
     */
    Vert *operator[](const size_t &index) const { return verts[index]; }
};

/**
 * @class Mesh
 * @brief Mesh container class
 *
 * Main mesh data structure containing vertices, edges, faces, and bounding box.
 */
class Mesh {
  public:
    /**
     * @brief Default constructor
     * Initializes mode to "generic"
     */
    Mesh() { mode = "generic"; }

    std::string mode;          ///< Mesh mode (e.g., "generic")
    std::vector<Vert *> verts; ///< All vertices in the mesh
    std::vector<Edge *> edges; ///< All edges in the mesh
    std::vector<Face *> faces; ///< All faces in the mesh
    Bbox bbox;                 ///< Bounding box of the mesh
};

} // namespace Mesh
} // namespace meshTools
