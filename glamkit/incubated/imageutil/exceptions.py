class ImageMagickException(Exception):
  pass

class ImageMagickOSFileError(ImageMagickException):
  pass

class ImageMagickConversionError(ImageMagickException):
  pass