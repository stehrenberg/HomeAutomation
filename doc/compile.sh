#!/bin/bash
pandoc --template template.latex -Vlang=german --toc -s -f markdown+fenced_code_attributes+escaped_line_breaks+implicit_figures documentation.md -o doc.pdf
