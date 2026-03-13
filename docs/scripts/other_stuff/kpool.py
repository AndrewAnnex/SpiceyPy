#
# Import the CSPICE-Python interface.
#
import spiceypy


# Assign the path name of the meta kernel to META.
def kpool(META="kpool.tm"):
    #
    # Load the meta kernel then use KTOTAL to interrogate the SPICE
    # kernel subsystem.
    #
    spiceypy.furnsh(META)
    count = spiceypy.ktotal("ALL")
    print(f"Kernel count after load:        {count}\n")
    #
    # Loop over the number of files; interrogate the SPICE system
    # with spiceypy.kdata for the kernel names and the type.
    # 'found' returns a boolean indicating whether any kernel files
    # of the specified type were loaded by the kernel subsystem.
    # This example ignores checking 'found' as kernels are known
    # to be loaded.
    #
    for i in range(count):
        [file, type, source, handle] = spiceypy.kdata(i, "ALL")
        print("File   {0}".format(file))
        print("Type   {0}".format(type))
        print("Source {0}\n".format(source))
    #
    # Unload one kernel then check the count.
    #
    spiceypy.unload("kernels/spk/de405s.bsp")
    count = spiceypy.ktotal("ALL")
    #
    # The subsystem should report one less kernel.
    #
    print(f"Kernel count after one unload:  {count}\n")
    #
    # Now unload the meta kernel. This action unloads all
    # files listed in the meta kernel.
    #
    spiceypy.unload(META)
    #
    # Check the count; spiceypy should return a count of zero.
    #
    count = spiceypy.ktotal("ALL")
    print(f"Kernel count after meta unload: {count}")
    #
    # Done. Unload the kernels.
    #
    spiceypy.kclear()


if __name__ == "__main__":
    kpool()
    kpool(META="kpool_generic.tm")
