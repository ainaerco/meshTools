/**
 * @file lists.h
 * @brief Template list class with additional operations
 */

#pragma once

#include <algorithm>
#include <vector>

namespace meshTools {
namespace Geometry {

/**
 * @class List
 * @brief A template list class extending std::vector with additional operations
 * @tparam T The type of elements stored in the list
 */
template <class T> class List : public std::vector<T> {
  public:
    /**
     * @brief Group duplicate elements from another list
     * @param l The list to compare with
     * @return Grouped element
     */
    T groupDuplicates(const List<T> &l);

    /**
     * @brief Find the index of an item in the list
     * @param item The item to find
     * @return Index of the item, or -1 if not found
     */
    unsigned int find(const T &item) const;
};

template <class T> T List<T>::groupDuplicates(const List<T> &l) {}

template <class T> unsigned int List<T>::find(const T &item) const {
    typename List<T>::iterator h = std::find(this->begin(), this->end(), item);

    return -1;
}

} // namespace Geometry
} // namespace meshTools
