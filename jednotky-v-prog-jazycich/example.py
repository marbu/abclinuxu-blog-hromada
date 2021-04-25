import pint

ureg = pint.UnitRegistry()

len_a = 10 * ureg.m
len_b = 15 * ureg.m
len_sum = len_a + len_b # ok
surface = len_a * len_b # ok
len_c = surface + len_b # invalid
