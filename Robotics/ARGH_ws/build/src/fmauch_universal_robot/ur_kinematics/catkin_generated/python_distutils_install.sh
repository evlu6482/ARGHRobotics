#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/argh/Documents/ARGH/ARGHRobotics/Robotics/ARGH_ws/src/src/fmauch_universal_robot/ur_kinematics"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/argh/Documents/ARGH/ARGHRobotics/Robotics/ARGH_ws/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/argh/Documents/ARGH/ARGHRobotics/Robotics/ARGH_ws/install/lib/python2.7/dist-packages:/home/argh/Documents/ARGH/ARGHRobotics/Robotics/ARGH_ws/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/argh/Documents/ARGH/ARGHRobotics/Robotics/ARGH_ws/build" \
    "/usr/bin/python2" \
    "/home/argh/Documents/ARGH/ARGHRobotics/Robotics/ARGH_ws/src/src/fmauch_universal_robot/ur_kinematics/setup.py" \
     \
    build --build-base "/home/argh/Documents/ARGH/ARGHRobotics/Robotics/ARGH_ws/build/src/fmauch_universal_robot/ur_kinematics" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/argh/Documents/ARGH/ARGHRobotics/Robotics/ARGH_ws/install" --install-scripts="/home/argh/Documents/ARGH/ARGHRobotics/Robotics/ARGH_ws/install/bin"
