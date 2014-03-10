#!/bin/sh

python2 pyclicker.py&
if hash i3-msg 2>/dev/null; then
  sleep 1
  i3-msg '[title="^PyClicker$"] floating enable'
fi
