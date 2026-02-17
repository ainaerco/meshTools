#ifndef _MESHTOOLS_LIST_H
#define _MESHTOOLS_LIST_H

#include <algorithm>
#include <vector>

namespace meshTools {
namespace Geometry {

template <class T> class List : public std::vector<T> {
  public:
    T group_duplicates(const List<T> &l);
    unsigned int find(const T &item) const;
};

template <class T> T List<T>::group_duplicates(const List<T> &l) {}

template <class T> unsigned int List<T>::find(const T &item) const {
    typename List<T>::iterator h = std::find(this->begin(), this->end(), item);

    return -1;
}

} // namespace Geometry
} // namespace meshTools

#endif