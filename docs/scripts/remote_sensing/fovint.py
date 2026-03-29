#
# Solution fovint.py
#
import spiceypy


def fovint(utctim="2004 jun 11 19:32:00"):
    METAKR = "fovint.tm"
    spiceypy.furnsh(METAKR)
    print(f"Converting UTC Time: {utctim}")
    et = spiceypy.str2et(utctim)
    print(f"  ET seconds past J2000: {et:16.3f}\n")
    # Obtain the NAIF ID and FOV configuration for the ISS NAC camera.
    try:
        nacid = spiceypy.bodn2c("CASSINI_ISS_NAC")
    except spiceypy.SpiceyError:
        print("Unable to locate the ID code for CASSINI_ISS_NAC")
        raise

    # getfov returns boundary corner vectors; append the boresight so we
    # can iterate over all vectors uniformly.
    shape, insfrm, bsight, n, bounds = spiceypy.getfov(nacid, 4)
    bounds = bounds.tolist()
    bounds.append(bsight)

    vec_names = [
        "Boundary Corner 1",
        "Boundary Corner 2",
        "Boundary Corner 3",
        "Boundary Corner 4",
        "Cassini NAC Boresight",
    ]

    # Shape model methods for sincpt and illumf — note that some SPICE
    # routines require different method strings; see each routine's docs.
    shape_models = ["Ellipsoid", "DSK/Unprioritized"]

    # Obtain the NAIF ID for Phoebe (needed for local solar time).
    try:
        phoeid = spiceypy.bodn2c("PHOEBE")
    except spiceypy.SpiceyError:
        print("Unable to locate the body ID code for Phoebe.")
        raise

    # For each FOV vector, intersect with Phoebe using both shape models.
    for i, (vec_name, vec) in enumerate(zip(vec_names, bounds)):
        print(f"Vector: {vec_name}\n")
        is_boresight = i == len(vec_names) - 1
        for shape_model in shape_models:
            print(f" Target shape model: {shape_model}\n")
            try:
                point, trgepc, srfvec = spiceypy.sincpt(
                    shape_model,
                    "PHOEBE",
                    et,
                    "IAU_PHOEBE",
                    "LT+S",
                    "CASSINI",
                    insfrm,
                    vec,
                )

                # Display the intercept position in the IAU_PHOEBE frame.
                print(
                    "  Position vector of surface intercept "
                    "in the IAU_PHOEBE frame (km):"
                )
                print(f"     X   = {point[0]:16.3f}")
                print(f"     Y   = {point[1]:16.3f}")
                print(f"     Z   = {point[2]:16.3f}")

                # Display planetocentric coordinates of the intercept.
                radius, lon, lat = spiceypy.reclat(point)
                dpr = spiceypy.dpr()
                print("  Planetocentric coordinates of the intercept (degrees):")
                print(f"     LAT = {lat * dpr:16.3f}")
                print(f"     LON = {lon * dpr:16.3f}")

                # Compute illumination angles at the intercept point.
                trgepc, srfvec, phase, solar, emissn, visibl, lit = spiceypy.illumf(
                    shape_model,
                    "PHOEBE",
                    "SUN",
                    et,
                    "IAU_PHOEBE",
                    "LT+S",
                    "CASSINI",
                    point,
                )

                print(f"  Phase angle (degrees):           {phase  * dpr:16.3f}")
                print(f"  Solar incidence angle (degrees): {solar  * dpr:16.3f}")
                print(f"  Emission angle (degrees):        {emissn * dpr:16.3f}")
                print(f"  Observer visible:  {visibl}")
                print(f"  Sun visible:       {lit}")

                # For the boresight vector, also compute local solar time.
                if is_boresight:
                    hr, mn, sc, time, ampm = spiceypy.et2lst(
                        trgepc, phoeid, lon, "PLANETOCENTRIC"
                    )
                    print(
                        f"\n  Local Solar Time at boresight "
                        f"intercept (24 Hour Clock):\n     {time}"
                    )

            except spiceypy.SpiceyError as exc:
                # Treat as no intersection found; continue with next vector.
                print(f"Exception message is: {exc.value}")

            print()

    spiceypy.unload(METAKR)


fovint()
