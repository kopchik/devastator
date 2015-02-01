#!/bin/bash

OUT="./build"
mkdir -p "$OUT"
duo ./site.src.css -S > "${OUT}/site.css"
duo ./site.src.js -S > "${OUT}/site.js"
