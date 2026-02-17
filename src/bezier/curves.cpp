#include "curves.h"

namespace curves {

float b(float t)
/* This function evaluates the uniform cubic B-spline. */
{
    float tp2, tp1, tm2, tm1;

    if (t <= -2.0f)
        return 0.0f;
    else if (t <= -1.0f) {
        tp2 = t + 2.0f;
        return tp2 * tp2 * tp2 / 6.0f;
    } else if (t <= 0.0f) {
        tp2 = t + 2.0f;
        tp1 = t + 1.0f;
        tp2 = tp2 * tp2 * tp2 / 6.0f;
        tp1 = 2.0f * tp1 * tp1 * tp1 / 3.0f;
        return tp2 - tp1;
    } else if (t <= 1.0) {
        tm1 = 1.0f - t;
        tm2 = 2.0f - t;
        tm1 = 2.0f * tm1 * tm1 * tm1 / 3.0f;
        tm2 = tm2 * tm2 * tm2 / 6.0f;
        return tm2 - tm1;
    } else if (t <= 2.0f) {
        tm2 = 2.0f - t;
        return tm2 * tm2 * tm2 / 6.0f;
    } else
        return 0.0f;
}

std::vector<float> Bezier::interpolate(const size_t &desired_num) {

    std::vector<float> res;
    mNumPoints = mPoints.size();
    size_t n;
    /* Make sure number of points is one more than a multiple of 3. */
    n = mNumPoints / 3 + (mNumPoints % 3) / 2;

    float delta_t = float(n / 3 + 1) / float(desired_num - 1);
    /* Construct Bezier curves for each grouping of four points. */
    // std::cout << " delta_t " << delta_t << " desired_num " << desired_num <<
    // "\n";
    size_t count = 0;
    for (size_t i = 0; i < n + 1; i += 3) {
        float ax, bx, cx, dx, ay, by, dy, cy, x, y;
        float mPointsI3x;
        float mPointsI3y;
        if (mNumPoints % 3 == 0 && (i + 3) * 2 > mNumPoints - 2) {
            mPointsI3x = mPoints.at(mNumPoints - 2);
            mPointsI3y = mPoints.at(mNumPoints - 1);
        } else {
            mPointsI3x = mPoints.at((i + 3) * 2);
            mPointsI3y = mPoints.at((i + 3) * 2 + 1);
        }
        ax = -mPoints.at(i * 2) +
             3.0f * (mPoints.at((i + 1) * 2) - mPoints.at((i + 2) * 2)) +
             mPointsI3x;
        ay =
            -mPoints.at(i * 2 + 1) +
            3.0f * (mPoints.at((i + 1) * 2 + 1) - mPoints.at((i + 2) * 2 + 1)) +
            mPointsI3y;
        bx = 3.0f * (mPoints.at(i * 2) - 2.0f * mPoints.at((i + 1) * 2) +
                     mPoints.at((i + 2) * 2));
        by =
            3.0f * (mPoints.at(i * 2 + 1) - 2.0f * mPoints.at((i + 1) * 2 + 1) +
                    mPoints.at((i + 2) * 2 + 1));
        cx = -3.0f * (mPoints.at(i * 2) - mPoints.at((i + 1) * 2));
        cy = -3.0f * (mPoints.at(i * 2 + 1) - mPoints.at((i + 1) * 2 + 1));
        x = dx = mPoints.at(i * 2);
        y = dy = mPoints.at(i * 2 + 1);
        // std::cout << "i  " << i << "\n";
        // std::cout << x << "   " << y << "\n";
        res.push_back(x);
        res.push_back(y);
        count++;
        for (float t = delta_t; t < 1.0f - EPSILON; t += delta_t) {

            x = ((ax * t + bx) * t + cx) * t + dx;
            y = ((ay * t + by) * t + cy) * t + dy;
            // std::cout << " t " << t <<" " << x << "   " << y << "\n";
            res.push_back(x);
            res.push_back(y);
            count++;
        }
    }
    res.push_back(mPoints.at(mNumPoints - 2));
    res.push_back(mPoints.at(mNumPoints - 1));
    // std::cout << "count  " << count << "\n";
    return res;
}

std::vector<float> Lagrange::interpolate(const size_t &desired_num) {
    std::vector<float> res;
    mNumPoints = mPoints.size();
    float delta_t = 0.1f;
    /* Handle first set of 4 points between t=-1 and t=0 separately. */
    for (float t = -1.0f; t < delta_t / 2.0f; t += delta_t) {
        float x, y;
        float b1 = B(1, t);
        float b2 = B(2, t);
        float b3 = B(3, t);
        float b4 = B(4, t);
        // 			x = px[0]*b1 + px[1]*b2 +
        // 			    px[2]*b3 + px[3]*b4;
        // 			y = py[0]*b1 + py[1]*b2 +
        // 			    py[2]*b3 + py[3]*b4;
        x = mPoints.at(0) * b1 + mPoints.at(2) * b2 + mPoints.at(4) * b3 +
            mPoints.at(6) * b4;
        y = mPoints.at(1) * b1 + mPoints.at(3) * b2 + mPoints.at(5) * b3 +
            mPoints.at(7) * b4;
        // std::cout << x << "  " << y << "\n";
        res.push_back(x);
        res.push_back(y);
    }

    /* Handle middle segments. */

    for (size_t i = 1; i <= mNumPoints / 3; i++) {
        // std::cout << i << "\n";
        for (float t = delta_t; t < 1.0f + delta_t / 2.0f; t += delta_t) {
            float x, y;
            float b1 = B(1, t);
            float b2 = B(2, t);
            float b3 = B(3, t);
            float b4 = B(4, t);
            // x = px[i - 1] * b1 + px[i] * b2 + px[i + 1] * b3 + px[i + 2] *
            // b4; y = py[i - 1] * b1 + py[i] * b2 + py[i + 1] * b3 + py[i + 2]
            // * b4;
            x = mPoints.at((i - 1) * 2) * b1 + mPoints.at(i * 2) * b2 +
                mPoints.at((i + 1) * 2) * b3 + mPoints.at((i + 2) * 2) * b4;
            y = mPoints.at((i - 1) * 2 + 1) * b1 + mPoints.at(i * 2 + 1) * b2 +
                mPoints.at((i + 1) * 2 + 1) * b3 +
                mPoints.at((i + 2) * 2 + 1) * b4;
            // std::cout << x << "  " << y << "\n";
            res.push_back(x);
            res.push_back(y);
        }
    }

    /* Handle the last set of 4 points between t=1.0 and t=2.0 separately. */

    for (float t = 1.0f + delta_t; t < 2.0f + delta_t / 2.0f; t += delta_t) {
        float x, y;
        float b1 = B(1, t);
        float b2 = B(2, t);
        float b3 = B(3, t);
        float b4 = B(4, t);
        x = mPoints.at(mNumPoints - 8) * b1 + mPoints.at(mNumPoints - 6) * b2 +
            mPoints.at(mNumPoints - 4) * b3 + mPoints.at(mNumPoints - 2) * b4;
        y = mPoints.at(mNumPoints - 7) * b1 + mPoints.at(mNumPoints - 5) * b2 +
            mPoints.at(mNumPoints - 3) * b3 + mPoints.at(mNumPoints - 1) * b4;
        // x = px[number_of_points-4]*b1 + px[number_of_points-3]*b2 +
        //     px[number_of_points-2]*b3 + px[number_of_points-1]*b4;
        // y = py[number_of_points-4]*b1 + py[number_of_points-3]*b2 +
        //     py[number_of_points-2]*b3 + py[number_of_points-1]*b4;
        // std::cout << x << "  " << y << "\n";
        res.push_back(x);
        res.push_back(y);
    }
    return res;
}

float *Spline1::interpolate(float *mPoints, const size_t &mNumPoints,
                            size_t &numPoints) {
    float delta_t = 1 / float(numPoints);
    float *res = new float[numPoints * numPoints / 2];
    float *points = new float[mNumPoints + 8];
    numPoints = 0;
    /* Load local arrays with data and make the two endpoints multiple so that
     * they are interpolated. */

    *(points) = *(points + 2) = *(mPoints);
    *(points + 1) = *(points + 3) = *(mPoints + 1);
    for (size_t i = 0; i < mNumPoints / 2; i++) {
        *(points + (i + 2) * 2) = *(mPoints + i * 2);
        *(points + (i + 2) * 2 + 1) = *(mPoints + i * 2 + 1);
    }
    *(points + mNumPoints + 4) = *(points + mNumPoints + 6) =
        *(mPoints + mNumPoints - 2);
    *(points + mNumPoints + 5) = *(points + mNumPoints + 7) =
        *(mPoints + mNumPoints - 1);

    /* Compute the values to plot. */
    for (size_t i = 0; i <= mNumPoints / 2; i++) {
        for (float t = delta_t; t < 1.0f + delta_t / 2.0f; t += delta_t) {
            float bt1 = b(t - 2.0f);
            float bt2 = b(t - 1.0f);
            float bt3 = b(t);
            float bt4 = b(t + 1.0f);
            float x = *(points + i * 2) * bt4 + *(points + (i + 1) * 2) * bt3 +
                      *(points + (i + 2) * 2) * bt2 +
                      *(points + (i + 3) * 2) * bt1;
            float y = *(points + i * 2 + 1) * bt4 +
                      *(points + (i + 1) * 2 + 1) * bt3 +
                      *(points + (i + 2) * 2 + 1) * bt2 +
                      *(points + (i + 3) * 2 + 1) * bt1;

            *(res + numPoints) = x;
            numPoints++;
            *(res + numPoints) = y;
            numPoints++;
        }
    }
    delete[] points;
    return res;
}

std::vector<float> Spline::interpolate(const size_t &desired_num) {
    std::vector<float> res;
    mNumPoints = mPoints.size();
    float delta_t = 1 / float(desired_num);
    std::vector<float> points;
    points.resize(mNumPoints + 8);

    /* Load local arrays with data and make the two endpoints multiple so that
     * they are interpolated. */

    points[0] = points[2] = mPoints.at(0);
    points[1] = points[3] = mPoints.at(1);
    for (size_t i = 0; i < mNumPoints / 2; i++) {
        points[(i + 2) * 2] = mPoints.at(i * 2);
        points[(i + 2) * 2 + 1] = mPoints.at(i * 2 + 1);
    }

    points[mNumPoints + 4] = points[mNumPoints + 6] =
        mPoints.at(mNumPoints - 2);
    points[mNumPoints + 5] = points[mNumPoints + 7] =
        mPoints.at(mNumPoints - 1);

    /* Compute the values to plot. */
    for (size_t i = 0; i <= mNumPoints / 2; i++) {
        for (float t = delta_t; t < 1.0f + delta_t / 2.0f; t += delta_t) {
            float bt1 = b(t - 2.0f);
            float bt2 = b(t - 1.0f);
            float bt3 = b(t);
            float bt4 = b(t + 1.0f);
            float x = points[i * 2] * bt4 + points[(i + 1) * 2] * bt3 +
                      points[(i + 2) * 2] * bt2 + points[(i + 3) * 2] * bt1;
            float y = points[i * 2 + 1] * bt4 + points[(i + 1) * 2 + 1] * bt3 +
                      points[(i + 2) * 2 + 1] * bt2 +
                      points[(i + 3) * 2 + 1] * bt1;
            res.push_back(x);
            res.push_back(y);
        }
    }
    return res;
}

} // namespace curves
