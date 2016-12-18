from utopyiad import Utopyia

ut= Utopyia("mock")
rep= dict(ut.all_replicates.items()).keys()[0]
ut.init_alignment(rep)



