# Directory to watch for file drops
watchdir = './img'

# Thread count to use for compressing images, also determines batch size
# Options are: [int], 'auto'
threads = 1

# MongoDB DB name
dbname = 'lilpicd'

# Flag removal of exif/meta data
stripexif = True

compressutils = {'png' :[
						'zopflipng',
						#'optipng',
						#'advdef',#redundant with zopflipng or advpng, this tool is part of advancecomp
						#'advpng',#redundant with zopflipng or advdef
						],
				
				'jpeg' :[
						 'jpegtran',
						 #'cjpeg',#redundant with jpegtran, this tool is part of mozjpeg
						 ],
				
				'gif'  :[
						 'gifsicle',
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
							 '-optimize',
							 '-trim',				#nearly perfect but technically lossy
							 '-progressive',
							 '{filename}',
							 ],
				'cjpeg'    :[
							 '-optimize',
							 '-quality 90', 		#this is lossy, defaults to 75 if not set
							 '-progressive',
							 '{filename}',
							 ],
				}
