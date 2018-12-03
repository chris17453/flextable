# -*- coding: utf-8 -*-

from colors import colors,attributes,reset

#def load(name=Default):
    #yaml=None
    #with open(name, 'r') as stream:
    #    try:
    #        yaml=yaml.load(stream)
    #    except yaml.YAMLError as ex:
    #        raise Exception ("Error loading yaml {}".format(ex))
    #

class style:
    def __init__(self):
        self.whitespace=''
        self.line_ending='LRCF'
        self.color=modes()
        self.characters=characters(self.color.default)
  

# Helper classes
class color:
    def __init__(self,foreground=None,background=None,text=None,dim=None,bold=None,default=None):
        self.foreground=foreground
        self.background=background
        self.dim=dim
        self.bold=bold
        self.reset=reset.ALL
        #override missing colors
        if None != default :
            if None== foreground:
                foreground=default.foreground
            if None== background:
                background=default.background
            if None== dim:
                dim=default.dim
            if None == bold:
                bold=default.bold
                
        #print foreground,background,dim,bold
        self.color=colors(foreground=foreground,background=background,dim=dim,bold=bold)
        if None !=text:
            if text.rstrip()=='':
                text=None
        self.text=text
                
    
    def render(self,text=None,length=None,fill_character=' ',override=None):
        if text==None:
            text=self.text

  
        if None == text:
            text=''
            #TODO tabstop/tab
        
        # make safe
        text=u'{}'.format(text)
        text=text.replace('\t','       ')
        
        text=text.rstrip()
        if length!=None:
            text=text[:length].ljust(length,fill_character)
        if None!=override:
            return u"{0}{1}".format(override.color,text)    
        return u"{0}{1}{2}".format(self.color,text,self.reset)




class modes:
    def __init__(self):
        self.default  =color('blue'      )
        self.error    =color('red'        ,bold=True,default=self.default)
        self.overflow =color('yellow'     ,default=self.default)
        self.comment  =color('yellow'     ,default=self.default)
        self.data     =color('light gray' ,default=self.default)
        self.active   =color('white'      ,default=self.default)
        self.edit     =color('cyan'       ,default=self.default)
        self.disabled =color('dark gray'  ,default=self.default)


class characters:
    class char_walls:
        def __init__(self,default=None):
            self.left   =color(text=u'║',default=default)
            self.right  =color(text=u'║',default=default)
            self.top    =color(text=u'═',default=default)
            self.bottom =color(text=u'═',default=default)
    class char_center:
        def __init__(self,default=None):
            self.center = color(text=u'╬',default=default)
            self.left   = color(text=u'╠',default=default)
            self.right  = color(text=u'╣',default=default)
    
    class char_bottom:
        def __init__(self,default=None):
            self.left   = color(text=u'╚',default=default)
            self.center = color(text=u'╩',default=default)
            self.right  = color(text=u'╝',default=default)
    class char_top:
        def __init__(self,default=None):
            self.left   = color(text=u'╔',default=default)
            self.right  = color(text=u'╗',default=default)
            self.center = color(text=u'╦',default=default)
    class char_header:
        def __init__(self,default=None):
            self.left   = color(text=u'╡',default=default,foreground='White')
            self.right  = color(text=u'╞',default=default,foreground='White')
            self.center = color(text=u' ',default=default,foreground='green')
    class char_mid_header:
        def __init__(self,default=None):
            self.left   = color(text=u'-',default=default,foreground='White')
            self.right  = color(text=u'-',default=default,foreground='White')
            self.center = color(text=u' ',default=default,foreground='green')
    class char_footer:
        def __init__(self,default=None):
            self.left   = color(text=u'[',default=default,foreground='White') #╡
            self.right  = color(text=u']',default=default,foreground='White') #╞
            self.center = color(text=u' ',default=default,foreground='green')

    def __init__(self,default=None):
        self.walls      =self.char_walls(default=default)
        self.center     =self.char_center(default=default)
        self.bottom     =self.char_bottom(default=default)
        self.top        =self.char_top(default=default)
        self.header     =self.char_header(default=default)
        self.mid_header =self.char_mid_header(default=default)
        self.footer     =self.char_footer(default=default)


