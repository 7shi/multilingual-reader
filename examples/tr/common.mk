CORE_LANGS  = fr es de ja zh
EXTRA_LANGS = eo hi \
			  te kn tr et sr \
			  ko \
			  fi hu bg \
			  ta id ar \
			  fa ur he \
			  it pt ru uk pl cs nl sv ia \
			  el ca ro vi lv lt ml \
			  bn th ms da no is hr sk sl \
			  sw cy eu hy ka km my sq af gl \
			  tl mk az mr ne be ga lo mn si

# PLaMo 3 Translate: the languages its model card lists as supported, all but the source
# English. The corpus's first (zh is sent as zh-hans by trtools plamo), then the ones the
# corpus lacks, which the comparison with other models cuts. The corpus's others came out
# in another language, mixed or collapsed (experimental/16).
PLAMO_LANGS = fr es de ja zh hi te et sr ko hu bg ta id ar fa ur he it ru pl nl \
			  ca vi lv lt ml bn th ms hr sk sl sw eu hy ka km my az mr ne be tl si \
			  zh-hant ceb gu jv kk pa uz
