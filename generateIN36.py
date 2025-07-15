
def towrite(m):
    if m >= 0 and m < 8:

        mainstr = f"""200-90 0 2  01.  0.2    5.E-08    1.E-11-2 00190 0 1.0  0.65  0.0 1.00   -6
        50    {m+6}Sn{m+5}+   4p64d{9-m}           3d10 4s2 4p6 4d{9-m}
        50    {m+6}Sn{m+5}+   4p54d{10-m}          3d10 4s2 4p5 4d{10-m}
        50    {m+6}Sn{m+5}+   4d{8-m}4f1           3d10 4s2 4p6 4d{8-m} 4f1
    -1"""
    elif m == 8:
        mainstr = f"""200-90 0 2  01.  0.2    5.E-08    1.E-11-2 00190 0 1.0  0.65  0.0 1.00   -6
   50   14Sn13+  4p64d1           3d10 4s2 4p6 4d1
   50   14Sn13+  4p54d2           3d10 4s2 4p5 4d2
   50   14Sn13+  4p64f1           3d10 4s2 4p6 4f1
   -1
"""
    else:
        raise Exception("invalid m value")
        
    return mainstr

for i in range(0, 9):
    mainstr = towrite(i)
    filename = f"C:\\Users\\brewster\\Desktop\\CowanFrontend\\InputOutputCowan\\IN36_{i}"
    with open(filename, "w") as f:
        f.write(mainstr)


