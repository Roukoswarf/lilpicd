# Directory to watch for file drops
watchdir = './img/test'

# Directory to write the finished files to
writedir = './img/wankers'

# Thread count to use for compressing images, also determines batch size
# Options are: [int], 'auto'
threads = 1

# MongoDB DB name
dbname = 'lilpicd'

# Flag removal of exif/meta data
stripexif = True

pillowargs = 	{'png'	:[
						#'optimize=True', #potentially redundant with png, lossless
						'compress_level=0' #ignored if -optimize is enabled 
				],

				'jpeg'	:[
						'quality=90',#lossy, lower numbers will result in lower quality with smaller file sizes
						'optimize=True',
						'progressive=True'
				],

				'gif' 	:[
						'optimize=True'
				]
}
compressutils = {'png' :[
						'zopflipng',#best tool
						#'optipng', #second best tool
						#'advdef',  #redundant with zopflipng or advpng, this tool is part of advancecomp
						#'advpng',  #redundant with zopflipng or advdef
						],
				
				'jpeg' :[
						 #'jpegtran', #redundant with pillow, lowers quality, not worth using
						 ],
				
				'gif'  :[
						 #'gifsicle', #redundant with pillow
						 ],
				}
compressargs = {
				'gifsicle' :[
							'-b',
							'-o3',
							'{filename}',
							],

				'exiftool' :[
							'-overwrite_original_in_place',
							'-all=',
							'{filename}',
							],
				
				'advdef'   :[
							'-z4',
							'{filename}',
							],
				
				'advpng'   :[
							'-z4',
							'{filename}',
							],
				
				'optipng'  :[
							'-o4',
							'{filename}',
							],
				
				'zopflipng':[
							 #'-m',					#this is doubles time
							 #'--splitting=3',		#this is doubles time
							 '--lossy_transparent', #loses invisible data
							 '-y',					#mandatory
							 '{filename}',
							 '{filename}',
							 ],
							 
				'jpegtran' :[
							 '-copy', 'none',
							 '-optimize',
							 '-trim',				#nearly perfect but technically lossy
							 '-progressive',
							 '-outfile', '{filename}',
							 '{filename}',
							 ],
				}
