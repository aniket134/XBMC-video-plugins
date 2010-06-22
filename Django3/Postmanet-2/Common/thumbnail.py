import sys, os
import Image


def generate_thumbnail(srcFile,dstFile,size=(128,128)):
	"""generate thumbnail for srcFile and store it in dstFile. For now the size of the thumbnail is the default value (128,128).
	Also the format is dictated by the extension of dstFile."""
	try:
		im = Image.open(srcFile)
		im.thumbnail(size,Image.ANTIALIAS)
		im.save(dstFile)
		return True
	except IOError:
		print "Couldnt generate thumbnail for", srcFile  # change this to logging functionality later.
		return False

# def generate_thumbnail(infile,outfile,size,format):
# 	"""generate thumbnail for infile of size size in format format and store it in file outfile."""
# 	im = Image.open(infile)
# 	im.thumbnail(size,Image.ANTIALIAS)
# 	im.save(outfile,format)
# 
# def generate_thumbnail(infile,size,format):
# 	"""same as above except outfile name is generated based on infile"""
# 	file, ext = os.path.splitext(infile)
# 	generate_thumbnail(infile,file + "_thumbnail." + ext, size, format)
# 
# def generate_thumbnail(infile,outfile,size):
# 	"""generate thumbnail for infile of size size in format format and store it in file outfile."""
# 	im = Image.open(infile)
# 	im.thumbnail(size,Image.ANTIALIAS)
# 	im.save(outfile)
# 
# def generate_thumbnail(infile,outfile):
# 	generate_thumbnail(infile,outfile,(128,128))
# 
# def generate_thumbnail(infile, size):
# 	file, ext = os.path.splitext(infile)
# 	generate_thumbnail(infile, file + "_thumbnail." + ext, size)
# 
# def generate_thumbnail(infile):
# 	generate_thumbnail(infile,(128,128))
# 
# 
