import pyvctrl


def easy_vt(slope, niveau):
    """ A simple wrapper around pyvctrl.vt, using the
        room temperature and outside temperature in our
        local Vitodens200 location.
    """
    return pyvctrl.vt(23.0, 8.0, 8.0, slope, niveau)

def increased_vt(slope, niveau):
    """ Print a comparison line between slope/niveau/VLsoll before
        and after raising the values.
    """
    print("%f/%f => %f   %f/%f => %f" % (slope, niveau, easy_vt(slope, niveau),
                                         0.7, niveau+4.0, easy_vt(0.7, niveau+4.0)))

def main():
    # Simple test output
    print(pyvctrl.vt(23.0, 8.0, 8.0, 0.4, 24.0))
    print(pyvctrl.vt2(23.0, 8.0, 8.0, 0.4, 24.0))
    print("\n\n")
    # Compare different niveau/slope combinations
    # for what happens when we increase the slope to 0.7
    # and add 4K to the niveau.
    increased_vt(0.2, 24.0)
    increased_vt(0.4, 27.0)
    increased_vt(0.4, 30.0)
    increased_vt(0.4, 34.0)

if __name__ == "__main__":
    main()

