import sys
from cv import *
import Image


class detect:

	def inside(r, q):
		(rx, ry), (rw, rh) = r
		(qx, qy), (qw, qh) = q
		return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


	def coordinates(img):
		while True:


			found = list(HOGDetectMultiScale(img2, storage, win_stride=(8,8),
				padding=(32,32), scale=1.05, group_threshold=2))
			found_filtered = []
			for r in found:
				insidef = False
				for q in found:
					if inside(r, q):
						insidef = True
						break
				if not insidef:
					found_filtered.append(r)
			for r in found_filtered:
				(rx, ry), (rw, rh) = r
				tl = (rx + int(rw*0.1), ry + int(rh*0.07))
				br = (rx + int(rw*0.9), ry + int(rh*0.87))
				R=(tl,br)
				return R
			