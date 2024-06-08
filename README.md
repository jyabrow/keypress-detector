# keypress-detector
Demo code to illustrate pyqt/pynput thread conflict, and solution. Provides robust example code module to detect MacOS keypresses, including CMD and CTRL modified keys.

## Introduction
This repository accompanies an article on how I solved a thread conflict problem when working on an PyQt app that used pynput for global keypress events, along with a QTimer for asynchronous delays. See the article for a full explanation, but the basic problem was that when the pynput event handler attempts to call a PyQt method that in turn invokes a QTimer, the thread immediately halts and issues the message:

QObject::startTimer: Timers can only be used with threads started with QThread

The code in this repository are examples to reproduce and solve the problem. It was developed and tested on MacOS, may need to be modified for Windows or Linux.

The companion article is published [here](https://www.linkedin.com/pulse/custom-qt-signal-resolves-pyqtpyinput-thread-conflict-jeremy-yabrow-abtqc/)

## Code

* keypress-detector-problem.py - Minimal code to reproduce problem
* keypress-detector-signal.py - Code using custom signal to avoid problem
* keypress-detector-full.py - Code w/solution + more complete key detection

## Instructions

The code examples should be easy to run, just open a MacOS terminal shell, clone the repo, setup and activate a virtual environment, install dependencies, and run each .py file from the command line:

```
% mkdir -p workspace
% cd workspace
% git clone git@github.com:jyabrow/keypress-detector.git
% cd keypress-detector
% python -m venv venv`
% which python # (make sure python path is set to ./venv/...)
% source venv/bin/activate
% pip install PySide6
% pip install pynput
% python keypress-detector-problem.py
% python keypress-detector-signal.py
% python keypress-detector-full.py
```
