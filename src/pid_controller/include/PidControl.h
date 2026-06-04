#ifndef PIDCONTROL_H
#define PIDCONTROL_H

#include <algorithm>
#include <cmath>

namespace ebot_controller {

class PidControl {
public:
    PidControl() {
      last_error_ = 0.0; int_val_ = 0.0; last_int_val_ = 0.0;
      kp_ = 0.0; ki_ = 0.0; kd_ = 0.0; min_ = -INFINITY; max_ = INFINITY;
    }
    PidControl(double kp, double ki, double kd, double min, double max) {
      last_error_ = 0.0; int_val_ = 0.0; last_int_val_ = 0.0;
      kp_ = kp; ki_ = ki; kd_ = kd; min_ = std::min(min,max); max_ = std::max(min,max);
    }
    void set(double kp,double ki,double kd)
    {
      kp_ = kp;
      ki_ = ki;
      kd_ = kd;
    }

    void setGains(double kp, double ki, double kd) { kp_ = kp; ki_ = ki; kd_ = kd; }
    void setRange(double min, double max) { min_ = std::min(min,max); max_ = std::max(min,max); }
    void setParams(double kp, double ki, double kd, double min, double max) { setGains(kp,ki,kd); setRange(min,max); }
    void resetIntegrator() { int_val_ = 0.0; last_int_val_ = 0.0; }
    void revertIntegrator() { int_val_ = last_int_val_; }

    double step(double error) {
      return step(error, 1.0);
    }

    double step(double error, double dt) {
      if (dt <= 0.0 || std::isnan(dt)) {
        dt = 1.0;
      }
      last_int_val_ = int_val_;

      double integral = int_val_ + error * dt;
      double derivative = (error - last_error_) / dt;

      double y = kp_ * error + ki_ * integral + kd_ * derivative;
      // Output limitation.
      double limited = std::max(min_, std::min(max_, y));
      if (limited == y) {
        int_val_ = integral;
      }
      y = limited;
      last_y_ = y;
      last_error_ = error;
      return y;
    }

private:
    double last_error_;
    double int_val_, last_int_val_;
    double last_y_;
    double kp_, ki_, kd_;
    double min_, max_;

};

}

#endif // PIDCONTROL_H
