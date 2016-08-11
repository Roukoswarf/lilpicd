# directory to watch for file drops
watchdir = './img'

# thread count to use for compressing images, also determines batch size
# options are: [int], 'auto'
threads = 1

compressutils = {'png' :[
						'zopflipng',
						#'optipng',
						#'advdef',#redundant with zopflipng or advpng, this tool is part of advancecomp
						#'advpng',#redundant with zopflipng or advdef
						'exiftool'
						]

				'jpeg' :[
						 'jpegtran',
						 #'cjpeg',#redundant with jpegtran, this tool is part of mozjpeg
						 'exiftool'
						 ] 
				
				'gif'  :[
						 'gifsicle',
						 'exiftool'
						 ]
				}
compressargs = {
				'gifsicle' :[
							'-b',
							'-o3'
				]

				'exiftool' :['-all=']
				
				'advdef'   :['-z4']					
													
				'advpng'   :['-z4']					
				
				'optipng'  :['-o4']
				
				'zopflipng':[
							 #'-m',			   		#this is doubles time
							 #'--splitting=3', 		#this is doubles time
							 '--lossy_transparent'  #loses invisible data
							 '--prefix'				#mandatory
							 ]			
							 
				'jpegtran' :[
							 '-optimize',
							 '-trim',				#nearly perfect but technically lossy
							 '-progressive'
							 ]				
				'cjpeg'    :[
							 '-optimize', 			
							 '-quality 90', 		#this is lossy, defaults to 75 if not set
							 '-progressive'
							 ]
				}
