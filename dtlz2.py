# Copyright 2012-2014 The Pennsylvania State University
#
# This software was written by David Hadka and others.
#
# The use, modification and distribution of this software is governed by the
# The Pennsylvania State University Research and Educational Use License.
# You should have received a copy of this license along with this program.
# If not, contact <dmh309@psu.edu>.
from sys import *
from math import *

nvars = 11
nobjs = 2
k = nvars - nobjs + 1

while True:
	# Read the next line from standard input
	line = raw_input()

	# Stop if the Borg MOEA is finished
	if line == "":
		break

	# Parse the decision variables from the input
	vars = map(float, line.split())

	# Evaluate the DTLZ2 problem
	g = 0

	for i in range(nvars-k, nvars):
		g = g + (vars[i] - 0.5)**2

	objs = [1.0 + g]*nobjs

	for i in range(nobjs):
		for j in range(nobjs-i-1):
			objs[i] = objs[i] * cos(0.5 * pi * vars[j])
		if i != 0:
			objs[i] = objs[i] * sin(0.5 * pi * vars[nobjs-i-1])

	# Print objectives to standard output, flush to write immediately
	print " ".join(["%0.17f" % obj for obj in objs])
	stdout.flush()

