#!/bin/bash
pandoc -Vlang=german --toc -s -f markdown+escaped_line_breaks+implicit_figures documentation.md -o doc.pdf
