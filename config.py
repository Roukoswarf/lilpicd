# directory to watch for file drops
watchdir = './img'

# thread count to use for compressing images, also determines batch size
# options are: [int], 'auto'
threads = 1

compressutils = {'png': ['zopfli'],
				 'jpeg': ['jpegtran'],
				 'gif': ['gifsicle'],
				 }
compressargs = {'zopfli': ['-z 4'],
				'jpegtran': ['-optimize', '-trim', '-progressive'],
				'gifsicle': ['--optimize']
				}

#advpng -z 4

#jpegtran -optimize -trim -progressive

#gifscile  --optimize
