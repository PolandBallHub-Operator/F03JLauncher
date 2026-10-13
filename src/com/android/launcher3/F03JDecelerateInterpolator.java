package com.android.launcher3;

import android.animation.TimeInterpolator;

/** Public-SDK implementation matching android.view.animation.DecelerateInterpolator. */
final class F03JDecelerateInterpolator implements TimeInterpolator, android.view.animation.Interpolator {
    private final float factor;

    F03JDecelerateInterpolator(float factor) {
        this.factor = factor;
    }

    @Override
    public float getInterpolation(float input) {
        if (factor == 1.0f) {
            final float inverse = 1.0f - input;
            return 1.0f - inverse * inverse;
        }
        return 1.0f - (float) Math.pow(1.0f - input, 2.0f * factor);
    }
}
