"""
Created on Jun 21, 2017

@author: sfurman
"""


def twos_complement_chksum(bin_str):
    sum_bytes = sum(ord(c) for c in bin_str)
    chksum = -(sum_bytes % 256) & 0xff
    return chksum
