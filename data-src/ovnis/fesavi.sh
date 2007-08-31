mencoder mf://*.png -mf fps=25 -ovc lavc -lavcopts vpass=1:vbitrate=1500:vcodec=mpeg4 -o vifreevial.mpeg
mencoder mf://*.png -mf fps=25 -ovc lavc -lavcopts vpass=2:vbitrate=1500:vcodec=mpeg4 -o vifreevial.mpeg

