__author__ = 'ama6fy'
# C        STFH           File handle.
# C
# C        STPREV         Record number of previous array summary.
# C
# C        STTHIS         Record number of current array summary.
# C
# C        STNEXT         Record number of next array summary.
# C
# C        STNSEG         Number of summaries in current summary record.
# C
# C        STCURR         Index of current summary within summary record.
# C
# C        STNR           Last name record read.
# C
# C        STHVNR         Flag indicating whether name record containing
# C                       name of current array is buffered.
# C
# C        STSR           Last summary record read.
# C
# C     These variables are maintained in a table of parallel arrays;
# C     the size of the table is TBSIZE.
# C
#       INTEGER               STFH   (         TBSIZE )
#       INTEGER               STPREV (         TBSIZE )
#       INTEGER               STTHIS (         TBSIZE )
#       INTEGER               STNEXT (         TBSIZE )
#       INTEGER               STNSEG (         TBSIZE )
#       INTEGER               STCURR (         TBSIZE )
#       CHARACTER*(CRLEN)     STNR   (         TBSIZE )
#       LOGICAL               STHVNR (         TBSIZE )
#       DOUBLE PRECISION      STSR   ( DPRSIZ, TBSIZE )


class SpiceDAF(object):
    def __init__(self):
        super().__init__()
        self.tbsize = 10
        self.STFH = [None] * self.tbsize
        self.STPREV = [None] * self.tbsize
        self.STTHIS = [None] * self.tbsize
        self.STNEXT = [None] * self.tbsize
        self.STNSEG = [None] * self.tbsize
        self.STCURR = [None] * self.tbsize
        self.STNR = [None] * self.tbsize
        self.STHVNR = [None] * self.tbsize
        self.STSR = [None] * self.tbsize
        self.STHEAD = 0
        self.STFPTR = 0

    def dafada(self):
        pass

    def dafarr(self):
        pass

    def dafarw(self):
        pass

    def dafbbs(self, handle):
        pass

    def dafbfs(self, handle):
        pass

    def dafbna(self):
        pass

    def dafcad(self):
        pass

    def dafcls(self, handle):
        pass

    def dafcs(self, handle):
        pass

    def dafena(self):
        pass

    def daffnh(self):
        pass

    def daffna(self, found):
        pass

    def daffpa(self, found):
        pass

    def dafgh(self):
        pass

    def dafgn(self):
        nd, ni = self.dafhsf(self.STFH[self.STHEAD])
        sumsize = nd + (ni + 1) // 2
        namesize = sumsize * 8
        offset = (self.STCURR[self.STHEAD] - 1) * namesize
        name = self.STNR[offset + 1:offset + namesize]
        return name

    def dafgs(self, insum):
        pass

    def dafhsf(self, something):
        #handle to summary format
        return 0, 0

    def dafwda(self):
        #write data to address
        pass

    def dafwdr(self):
        #write double precision record
        pass

    def dafhfn(self):
        #handle to file name
        pass

    def dafhlu(self):
        #handle to logical unit
        pass

    def dafhof(self):
        #handles of open files
        pass

    def dafluh(self):
        #logical unit to handle
        pass

    def dafnrr(self):
        #number of reads, requests
        pass

    def dafonw(self):
        #open new
        pass

    def dafopr(self):
        #open for read
        pass

    def dafopw(self):
        #open for write
        pass

    def dafps(self):
        #pack summary
        pass

    def dafra(self):
        #re - order arrays
        pass

    def dafrcr(self):
        #read character record
        pass

    def dafrda(self, handle, begin, end, data):
        #read data from address
        pass

    def dafrdr(self):
        #read double precision record
        pass

    def dafrfr(self):
        #read file record
        pass

    def dafrn(self):
        #replace name
        pass

    def dafrrr(self):
        #remove reserved records
        pass

    def dafrs(self):
        #replace summary
        pass

    def dafrwa(self):
        #record / word to address
        pass

    def dafsih(self):
        #signal invalid handles
        pass

    def dafus(self, insum, nd, ni, dc, ic):
        #unpack summary
        pass

    def dafwcr(self):
        #write character record
        pass

    def dafwfr(self):
        #write file record
        pass