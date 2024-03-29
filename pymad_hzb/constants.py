# ----------------------------------------------------------------
# MADX - Twiss columns as dictionary
# ----------------------------------------------------------------
MADtwissColumns = {}

MADtwissColumns['beta'] = ["NAME", "KEYWORD", "PARENT",
                           "S", "L", "BETX", "BETY"]
MADtwissColumns['coords'] = ["NAME", "KEYWORD", "PARENT",
                             "S", "L", "X", "PX", "Y", "PY", "T", "PT"]
MADtwissColumns['basic'] = ["NAME", "KEYWORD", "PARENT",
                            "S", "L", "X", "PX", "Y", "PY", "T", "PT",
                            "BETX", "BETY", "ALFX", "ALFY",
                            "MUX", "MUY",
                            "DX", "DY", "DPX", "DPY",
                            "HKICK", "VKICK",
                            "K0L", "K1L", "K1S", 'K2L']

MADtwissColumns["RMatrixExtended"] = ["NAME", "KEYWORD", "PARENT",
                                      "S", "L", "X", "PX", "Y", "PY", "T",
                                      "PT",
                                      "BETX", "BETY", "ALFX",
                                      "ALFY", "MUX", "MUY", "DX", "DY", "DPX",
                                      "DPY", "HKICK", "VKICK",
                                      "K0L", "K1L", "KMAX", "KMIN", "CALIB",
                                      "RE11", "RE12",
                                      "RE13", "RE14", "RE15", "RE16", "RE21",
                                      "RE22", "RE23", "RE24",
                                      "RE25", "RE26", "RE31", "RE32", "RE33",
                                      "RE34", "RE35", "RE36",
                                      "RE41", "RE42", "RE43", "RE44", "RE45",
                                      "RE46", "RE51", "RE52",
                                      "RE53", "RE54", "RE55", "RE56", "RE61",
                                      "RE62", "RE63", "RE64",
                                      "RE65", "RE66"]

MADtwissColumns["LHCTwiss"] = ["NAME", "KEYWORD", "PARENT", "S", "L",
                               "LRAD", "KICK", "HKICK", "VKICK", "ANGLE",
                               "K0L",
                               "K1L", "K2L",
                               "K3L", "X", "Y", "PX", "PY", "BETX", "BETY",
                               "ALFX", "ALFY", "MUX",
                               "MUY", "DX", "DY", "DPX", "DPY", "KMAX", "KMIN",
                               "CALIB",
                               "POLARITY", "APERTYPE", 'APER_1', 'APER_2',
                               'APER_3', 'APER_4', "N1", "TILT"]

MADtwissColumns["CTE"] = ["NAME", "S", "L", "BETX", "BETY", "ALFX", "ALFY",
                          "DX", "DPX", "DY", "DPY", "ANGL", "K1L",
                          "K1S"]

MADtwissColumns["all"] = ['NAME', 'KEYWORD', 'S',
                          'BETX', 'ALFX', 'MUX', 'BETY',
                          'ALFY', 'MUY', 'X', 'PX', 'Y', 'PY',
                          'T', 'PT', 'DX', 'DPX', 'DY', 'DPY', 'WX',
                          'PHIX', 'DMUX', 'WY', 'PHIY', 'DMUY', 'DDX',
                          'DDPX', 'DDY', 'DDPY', 'R11', 'R12', 'R21',
                          'R22', 'ENERGY', 'L', 'ANGLE', 'K0L', 'K0SL',
                          'K1L', 'K1SL', 'K2L', 'K2SL', 'K3L', 'K3SL',
                          'K4L', 'K4SL', 'K5L', 'K5SL', 'K6L', 'K6SL',
                          'K7L', 'K7SL', 'K8L', 'K8SL', 'K9L', 'K9SL',
                          'K10L', 'K10SL', 'K11L', 'K11SL', 'K12L',
                          'K12SL', 'K13L', 'K13SL', 'K14L', 'K14SL',
                          'K15L', 'K15SL', 'K16L', 'K16SL', 'K17L',
                          'K17SL', 'K18L', 'K18SL', 'K19L', 'K19SL',
                          'K20L', 'K20SL', 'KSI', 'HKICK', 'VKICK',
                          'TILT', 'E1', 'E2', 'H1', 'H2', 'HGAP',
                          'FINT', 'FINTX', 'VOLT', 'LAG', 'FREQ',
                          'HARMON', 'SLOT_ID', 'ASSEMBLY_ID', 'MECH_SEP',
                          'V_POS', 'LRAD', 'PARENT', 'RE11', 'RE12',
                          'RE13', 'RE14', 'RE15', 'RE16', 'RE21',
                          'RE22', 'RE23', 'RE24', 'RE25', 'RE26',
                          'RE31', 'RE32', 'RE33', 'RE34', 'RE35',
                          'RE36', 'RE41', 'RE42', 'RE43', 'RE44',
                          'RE45', 'RE46', 'RE51', 'RE52', 'RE53',
                          'RE54', 'RE55', 'RE56', 'RE61', 'RE62',
                          'RE63', 'RE64', 'RE65', 'RE66', 'KMAX',
                          'KMIN', 'CALIB', 'POLARITY', 'ALFA', 'BETA11',
                          'BETA12', 'BETA13', 'BETA21', 'BETA22',
                          'BETA23', 'BETA31', 'BETA32', 'BETA33',
                          'ALFA11', 'ALFA12', 'ALFA13', 'ALFA21',
                          'ALFA22', 'ALFA23', 'ALFA31', 'ALFA32',
                          'ALFA33', 'GAMA11', 'GAMA12', 'GAMA13',
                          'GAMA21', 'GAMA22', 'GAMA23', 'GAMA31',
                          'GAMA32', 'GAMA33', 'BETA11P', 'BETA12P',
                          'BETA13P', 'BETA21P', 'BETA22P', 'BETA23P',
                          'BETA31P', 'BETA32P', 'BETA33P', 'ALFA11P',
                          'ALFA12P', 'ALFA13P', 'ALFA21P', 'ALFA22P',
                          'ALFA23P', 'ALFA31P', 'ALFA32P', 'ALFA33P',
                          'GAMA11P', 'GAMA12P', 'GAMA13P', 'GAMA21P',
                          'GAMA22P', 'GAMA23P', 'GAMA31P', 'GAMA32P',
                          'GAMA33P', 'DISP1', 'DISP2', 'DISP3', 'DISP4',
                          'DISP1P', 'DISP2P', 'DISP3P', 'DISP4P', 'DISP1P2',
                          'DISP2P2', 'DISP3P2', 'DISP4P2', 'DISP1P3',
                          'DISP2P3', 'DISP3P3', 'DISP4P3', 'MU1', 'MU2',
                          'MU3', 'SIG11', 'SIG12', 'SIG13', 'SIG14',
                          'SIG15', 'SIG16', 'SIG21', 'SIG22', 'SIG23',
                          'SIG24', 'SIG25', 'SIG26', 'SIG31', 'SIG32',
                          'SIG33', 'SIG34', 'SIG35', 'SIG36', 'SIG41',
                          'SIG42', 'SIG43', 'SIG44', 'SIG45', 'SIG46',
                          'SIG51', 'SIG52', 'SIG53', 'SIG54', 'SIG55',
                          'SIG56', 'SIG61', 'SIG62', 'SIG63', 'SIG64',
                          'SIG65', 'SIG66', 'N1']

tfsheader = ['TYPE', 'SEQUENCE', 'PARTICLE', 'MASS',
             'CHARGE', 'ENERGY', 'PC', 'GAMMA', 'KBUNCH',
             'BCURRENT', 'SIGE', 'SIGT', 'NPART',
             'EX', 'EY', 'ET', 'LENGTH', 'ALFA', 'ORBIT5',
             'GAMMATR', 'Q1', 'Q2', 'DQ1', 'DQ2', 'DXMAX',
             'DYMAX', 'XCOMAX', 'YCOMAX', 'BETXMAX', 'BETYMAX',
             'XCORMS', 'YCORMS', 'DXRMS', 'DYRMS', 'DELTAP',
             'SYNCH_1', 'SYNCH_2', 'SYNCH_3', 'SYNCH_4', 'SYNCH_5',
             'TITLE', 'ORIGIN', 'DATE', 'TIME']
