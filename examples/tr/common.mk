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
# English, in alphabetical order (zh is sent as zh-hans by trtools plamo). Seven of them
# the corpus lacks (zh-hant ceb gu jv kk pa uz), which the comparison with other models
# cuts. The corpus's others came out in another language, mixed or collapsed
# (experimental/16).
PLAMO_LANGS = ar az be bg bn ca ceb de es et eu fa fr gu he hi hr hu hy id it ja jv \
			  ka kk km ko lt lv ml mr ms my ne nl pa pl ru si sk sl sr sw ta te th \
			  tl ur uz vi zh zh-hant
