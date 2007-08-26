"""
OpenGL 2D Font library.

This is a font library implementation for Python/OpenGL, it is designed to
plug-in to the Viper game engine but it also runs indepently.

The library renders fonts using the textured quads method. The primary goals in
developing the library where performance and flexibility, which comes at a
slight cost in memory due to the large number of draw arrays the class 
generates.

Colour, position, angle and scale can all be specified as well as smooth or
pixelated texture rendering.

The built-in cache option when calling the mWrite method supports for compiling
a draw array for the specified text which greatly improves performance for 
large amounts of text rendered multiple times.

Note: 
* True-type fonts are supported using the PIL (Python Imaging Library) - which 
can mean that render quality can suffer. Adjusting the font size a small amount
can often improves the quality.

* To run the demo please ensure the font file specified ('arial.ttf' by 
default) exists.

Modules required:
Pygame, PIL, PyOpenGL, and Psyco (used to improve performance, just comment it
out if you don't wish to use it).

Usage:
Use as you want but please credit me if you do, and/or email me and let me know
what your using it in:

Anthony Blackshaw <ant@getme.co.uk>, 2007.
"""

import psyco; psyco.full()
import pygame
import Image, ImageDraw, ImageFont
from OpenGL.GL import *
from OpenGL.GLU import *
    
    
class cFont:
    
    """
    A font class that supports the rendering of text in True-Type fonts (.ttf)
    to an OpenGL display.
    """
    
    def __init__( self, face, size, smooth = False ):
        
        """
        Initialise the font class.
        
        > face*
        The font file location (e.g. 'arial.ttf').
        
        > size*
        The size of the font in points.
        
        > smooth
        Use nearest (False) or linear (True) filtering when rendering 
        the font, use nearest unless you need to rotate or scale the font. 
        """
        
        # Make sure pygame is initialised
        pygame.display.init()

        # Define the font alphabet
        self.fontAlphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijsklmnopqrstuvwxyz{}()[]<>!?.,:;'\"*&%$@#\/|+=-_~`"
        
        # Determine the min/max texture size
        self._minFontSize = 32
        self._maxFontSize = glGetIntegerv( GL_MAX_TEXTURE_SIZE )
        
        # Default font colour
        self.colour = ( 255, 255, 255, 255 )
        
        # Create a text cache
        self._cache = {}
        
        # Load the font and create an image to render the character set to
        font = ImageFont.truetype( face, size )
        fontImage = Image.new( "L", ( self._minFontSize, self._minFontSize ) )
        fontDraw = ImageDraw.Draw( fontImage )
        fontDraw.setfont( font )
        
        # Specify some basic glyph information
        self._fontHeight = fontDraw.textsize( self.fontAlphabet )[ 1 ]
        self.lineHeight = self._fontHeight / 5.0 + self._fontHeight
        self.characterSpacing = 0.0
        self.wordSpacing = fontDraw.textsize( ' ' )[ 0 ]
        
        # Calculate the required size of the font image
        fontAlphabetSize = fontDraw.textsize( self.fontAlphabet )
        
        width = self._mNearestPowerOf2( fontAlphabetSize[ 0 ] )
        height = self._mNearestPowerOf2( fontAlphabetSize[ 1 ] )
        
        while width >= height:
            width /= 2
            height *= 2
        
        # Check for maximum size
        if width > self._maxFontSize:
            raise Exception( "Font size is too large" )
        
        # Resize the image
        fontImage = fontImage.resize( ( width, height ) )
        fontDraw = ImageDraw.Draw( fontImage )
        fontDraw.setfont( font )
        
        # Draw and map the font to an image
        x = 0
        y = 0

        self._characterUVMap = {}
        self._characterSizeMap = {}
        self._characterDrawArrayMap = {}
        
        for character in self.fontAlphabet:
            
            characterImage = font.getmask( character ).convert( 'L' )
            
            if x > fontImage.size[ 0 ] - characterImage.size[ 0 ]:
                x = 0
                y += self._fontHeight + 1
            
            self._characterUVMap[ character ] = ( 
                            float( x ) / float( fontImage.size[ 0 ] ), 
                            1.0 - ( float( y ) / float( fontImage.size[ 1 ] ) ), 
                            float( x + characterImage.size[ 0 ] ) / float( fontImage.size[ 0 ] ), 
                            1.0 - ( float( y + characterImage.size[ 1 ] ) / float( fontImage.size[ 1 ] ) )
                            )
            self._characterSizeMap[ character ] = ( characterImage.size[ 0 ], 0 - characterImage.size[ 1 ] )
            
            uv0, uv1, uv2, uv3 = self._characterUVMap[ character ]
            characterWidth, characterHeight = self._characterSizeMap[ character ]
            
            # Pre-render the mesh as a draw array
            self._characterDrawArrayMap[ character ] = glGenLists( 1 )
            glNewList( self._characterDrawArrayMap[ character ], GL_COMPILE )  
            
            glBegin( GL_QUADS )
            glTexCoord2f( uv0, uv1 )
            glVertex2f( 0, 0 )
            glTexCoord2f( uv2, uv1 )
            glVertex2f( characterWidth, 0 )
            glTexCoord2f( uv2, uv3 )
            glVertex2f( characterWidth, characterHeight )
            glTexCoord2f( uv0, uv3 )
            glVertex2f( 0, characterHeight )
            glEnd()
            
            glEndList()
        
            fontImage.paste( characterImage, ( x, y, x + characterImage.size[ 0 ], y + characterImage.size[ 1 ] ) )
                
            x += characterImage.size[ 0 ] + 1

        # Create a texture from the font
        self.texture = glGenTextures( 1 )
        glBindTexture( GL_TEXTURE_2D, self.texture )
        glPixelStorei( GL_UNPACK_ALIGNMENT, 1 )
        glTexImage2D( 
                GL_TEXTURE_2D, 
                0, 
                GL_ALPHA, 
                fontImage.size[ 0 ], 
                fontImage.size[ 1 ], 
                0, 
                GL_ALPHA, 
                GL_UNSIGNED_BYTE, 
                fontImage.tostring( "raw", "L", 0, -1 )
                )        

        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP )
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP )
        
        # Determine the texture interpolation when transformed
        if smooth:
            glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
            glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )        
        else:
            glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
            glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )
        
        glPrioritizeTextures( 1, self.texture, 1 );

        glDisable( GL_TEXTURE_2D )
        
        
    def __finalize__( self ):
        
        """
        Free the font instance.
        """
    
        # Free texture
        glDeleteTextures( cFont.texture )
        
        # Free display lists
        drawArrayList = cFont._characterDrawArrayMap.values()
        drawArrayList.sort()
    
        glDeleteLists( drawArrayList[ 0 ], len( drawArrayList ) )
        

    def _mNearestPowerOf2( self, value ):
        
        # Return the nearest power of two value for the specified value.
        
        newValue = 1
        while newValue < min( ( 16384, value ) ):
            newValue *= 2  
        
        return newValue        


    def mGetSize( self, text ):
        
        """
        Get the width and height of the specified text.
        
        > text*
        The text to get the size of.                
        """
        
        lineList = text.split( '\n' )
        maxWidth = 0
        
        _characterSizeMap = self._characterSizeMap
        characterSpacing = self.characterSpacing
        wordSpacing = self.wordSpacing
                
        for line in lineList:
            width = 0
            for character in line:
                if _characterSizeMap.has_key( character ):
                    width += _characterSizeMap[ character ][ 0 ] + characterSpacing
            else:
                width += wordSpacing                
            
            if width > maxWidth: maxWidth = width
                
        return ( maxWidth, self.lineHeight * len( text.split( '\n' ) ) )
    
    
    def mClearCache( self, text ):
        
        """
        Clear the cache of the specified text.
        
        > text*
        The text to clear the cache of.         
        """
        
        if self._cache.has_key( text ): del self._cache[ text ]
        
    
    def mWrite( self, text, position = ( 0, 0 ), angle = 0, scale = 1, cache = False ):
        
        """
        Render text to the screen.
        
        > text*
        The text to render to the screen.         
        
        > position
        The position to render the text at.
        
        > angle
        The angle to render the text at.        

        > scale
        The scale to render the text at.  

        > cache
        By specifing True for the cache the method will generate a draw array
        for rendering the complete text and will then use this to render the
        same text in future. 
                
        """
        
        # Get screen dimensions
        screenWidth = pygame.display.get_surface().get_width()
        screenHeight = pygame.display.get_surface().get_height()
        
        # Set the projection to 2D
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()
        gluOrtho2D( 0, screenWidth, 0, screenHeight )
        
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()
        
        # Position the text
        glTranslatef( position[ 0 ], screenHeight - position[ 1 ] + 1, 1.0 )
        glRotatef( angle, 0.0, 0.0, 1.0 )
        glScalef( scale, scale, 1.0 )  
        
        # Set the colour
        glColor4ub( *self.colour )

        # Select the font texture
        glEnable( GL_TEXTURE_2D )
        glBindTexture( GL_TEXTURE_2D, self.texture )

        # Render the text
        characterX = 0
        characterY = 0
        characterWidth = 0
        
        # Localise variables for performance
        _characterUVMap = self._characterUVMap
        _characterSizeMap = self._characterSizeMap
        _characterDrawArrayMap = self._characterDrawArrayMap
        _fontHeight = self._fontHeight
        characterSpacing = self.characterSpacing
        lineHeight = self.lineHeight
        wordSpacing = self.wordSpacing
        
        glPushMatrix()
        
        # Check for a chached versoin of the string
        if self._cache.has_key( text ):
            glCallList( self._cache[ text ] )
            
        else:
            
            if cache:
                self._cache[ text ] = glGenLists( 1 )
                glNewList( self._cache[ text ], GL_COMPILE )  
                
            for character in text:
                
                # Check the character can be rendered
                if _characterSizeMap.has_key( character ):
                
                    glTranslatef( characterWidth, 0, 0 )
                    characterWidth = _characterSizeMap[ character ][ 0 ] + characterSpacing
                    glCallList( _characterDrawArrayMap[ character ] )
                    characterX += characterWidth
                
                else:
                    
                    # Check for new line character
                    if character == '\n':
                        glTranslatef( 0 - characterX, 0 - lineHeight, 0 )
                        characterX = 0
                        characterY -= lineHeight
                        
                    else:
                        # Treat all non-renderable characters as a space ' '
                        glTranslatef( wordSpacing, 0, 0 )
                        characterX += wordSpacing
            if cache:
                glEndList()
                
        glPopMatrix()
        
        
def _dDemo():
    
    import sys
        
    # Set-up an OpenGL display via Pygame
    pygame.display.set_mode( ( 1024,768 ), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.OPENGL, 24 )

    # Create the font
    font1 = cFont( "gil.ttf", 15 )
    font1.colour = ( 255, 0, 0, 255 )

    font2 = cFont( "gil.ttf", 13, True )
    font2.colour = ( 0, 0, 0, 255 )    

    # Set the blend mode for the font ???
    glEnable( GL_BLEND )
    glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
    
    live = True
        
    while live:
            
        # Clear screen
        glClearColor( 255, 255, 255, 255 ) 
        glClear( GL_COLOR_BUFFER_BIT ) 
         
        # Render text
        #font1.mWrite( 'cFont - OpenGL font library', ( 10, 10 ) )
        font2.mWrite( __doc__, ( -10, 75 ), 22.5, 1.25, True )
        
        # Check for quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT: live = False        
        
        pygame.display.flip()

if __name__ == '__main__': _dDemo()         
