import sys
import select
import json
import os
import tempfile

from colors import *

def enum(**enums):
    return type('Enum', (), enums)

class table:
    data_type=enum(COMMENT=1,ERROR=2,DATA=3,WHITESPACE=4)
        
    def __init__(self,args=None):
        self.remove_quote=True
        self.block_quote=None
        self.column_count=0
        self.hide_comments=False
        self.hide_errors=False
        self.hide_whitespace=False
        self.starts_on_line=1
        self.header_on_line=0
        self.columns=None
        self.delimiters={'field':',',  'comment':'#'}
        self.length=None
        self.starts_on=1
        # TODO
        self.width='auto'
        # TODO
        # exapanding from fixed point
        self.tab_width=4
        # TODO
        # comments align on tabstops
        self.tab_stop=8

        if None !=args:
            self.args=args
            self.remove_quote=args.remove_quote
            self.block_quote==args.block_quote
                    
            self.header_on_line=args.header_on_line
            self.data_on_line=args.data_on_line
            self.hide_comments=args.hide_comments
            self.hide_errors=args.hide_errors
            self.hide_whitespace=args.hide_whitespace
            self.no_clip=False
            self.delimiters['field']=args.delimiter
            #auto name columns
            if args.column_count>-1:
                self.column_count=args.column_count
                self.columns=[]
                for n in range(0,self.column_count):
                    self.columns.append("column{}".format(n+1))
            
            
            if args.page>-1 and args.length>1:
                self.starts_on=args.page*args.length+1
            if self.args.line>-1:
                self.starts_on=args.line
            self.length=args.length

        else:
            self.args=None

        self.file=None
        self.is_temp_file=False
        self.results=[]
        self.format()

    def format_string(self,data,length,fill_character=' ',no_clip=False):
        if None == data:
            data=''
            #TODO tabstop/tab
            data=data.replace('\t','       ')
        data='{}'.format(data)
        if length==-1:
            return data
        if False==no_clip:
            return data[:length-2].ljust(length-2,fill_character)
        else:
            return data.ljust(length-2,fill_character)


    def process_line(self,line,line_number=0):
        err=None
        line_data=None
        if self.data_on_line>line_number:
            line_type=self.data_type.COMMENT
            line_data=[line]
        else:
            line_type=self.data_type.DATA
            if True == line.isspace():
                line_type=self.data_type.WHITESPACE
                line_data=[line]
            else:
                if line[0] is self.delimiters['comment']:
                    line_data=[line]
                    line_type=self.data_type.COMMENT
        
        return {'data':line_data,'type':line_type,'error':err}


    def process_data(self,line,line_number):
        err=None
        # ok its data. lets split it up and check for errors
        line_data=line.split(self.delimiters['field'])
        line_column_count=len(line_data)
        column_count=self.column_count

        # mark the row as an error and create a message if column counts are invalid, if there are column counts
        if None !=column_count:
            if line_column_count!=column_count:
                column_diff=column_count-line_column_count
                if column_diff>0:
                    err="Line #{0}, {1} extra Column(s)".format(line_number,column_diff)
                else:
                    err="Line #{0}, missing {1} Column(s)".format(line_number,column_diff*-1)
                
                line_type=self.data_type.ERROR
        # strip delimiters from field if block quoted (xlsx export to csv?)
        # if none just add the field
        if True == self.remove_quote:
            line_data_cleaned=[]
            for d in line_data:
                strip=False
                # block quote check, field must be > than 1 character
                if len(d)>1:
                    if d[0]=='"' and d[-1]=='"':
                        strip=True
                    else:
                        if d[0]=='\'' and d[-1]=='\'':
                            strip=True
                        else:
                            if None != self.block_quote:
                                if d[0]==self.block_quote and d[-1]==self.block_quote:
                                    strip=True

                if True==strip:
                    line_data_cleaned.append(d[1:-1])
                else:
                    line_data_cleaned.append(d)
            #swap ouyt the cleaned up row
            line_data=line_data_cleaned
        
        # update type if errored
        if None !=err:
            line_type=self.data_type.ERROR
        else:
            line_type=self.data_type.DATA

        return {'data':line_data,'type':line_type,'error':err}

    # loop through al lines in the stream and process
    def process_file(self):
        # offset dont get confused
        line_number=0
        visible_line=1
        buffer_length=0
        buffer=[]
        #print self.starts_on,self.length
        #exit(1)
        with open(self.file) as stream:
            for line in stream:
                line_number+=1
                
                # if columns are defined in the header, pull those
                if self.header_on_line==line_number:
                    results=self.process_line(line,line_number)
                    self.columns=results['data']
                    self.column_count=len(self.columns)
             

                # below visible window.. skip
                if  self.starts_on>=line_number:
                    continue

                results=self.process_line(line,line_number)
                    
                print line_number,results['type']
                # skip comments if asked to
                if results['type']==self.data_type.COMMENT and True == self.hide_comments: 
                    continue
                
                # skip errors if asked to
                if results['type']==self.data_type.ERROR and True == self.hide_errors: 
                    continue

                # skip errors if asked to
                if results['type']==self.data_type.WHITESPACE and True == self.hide_whitespace: 
                    continue

                print -1 == self.length , self.starts_on<=line_number-1,line_number,self.starts_on
                if results['type']==self.data_type.DATA: 
                    # only process visible data. saves a lot of string manipulation
                    results=self.process_data(line,line_number)
                    # skip errors if asked to
                    if results['type']==self.data_type.ERROR and True == self.hide_errors: 
                        continue
                

                # ok everything reaching here is wanted and visible
                buffer_length+=1
                visible_line+=1
                
                # if we are past our collection point... jet, lets not waste time here
                if -1 !=self.length and buffer_length>self.length:
                    break

                print line_number-1,self.starts_on,self.length
               
                results['visible_line_number']=visible_line
                results['file_line_number']=line_number
                results['raw']=line
                buffer.append(results)


        return buffer

    def build_header(self):
        tty_min_column_width=10
        #tty_rows, tty_columns = os.popen('stty size', 'r').read().split()
        tty_rows=30
        tty_columns=80
        data_column_count=self.column_count

        # no columns to return
        if data_column_count==0:
            self.column_character_width=-1
        else:
            if self.width=='auto':
                self.column_character_width=int(tty_columns)/data_column_count
                if self.column_character_width<tty_min_column_width:
                    self.column_character_width=tty_min_column_width
            else:
                self.column_character_width=int(width)

        self.total_width=self.column_character_width*data_column_count-1*data_column_count+1
        
        # header
        header=""
        header="{0}|{1}".format(bcolors.OKBLUE,bcolors.ENDC)
        
        if None != self.columns:
            for c in self.columns:
                if len(c)>self.column_character_width-2:
                    wall_color=bcolors.WARNING
                else:
                    wall_color=bcolors.OKBLUE
                
                display=c
                    
                header+="{3}{4}{0}{2}{1}|{2}".format(
                        self.format_string(display,self.column_character_width,' ',self.no_clip), #0
                        wall_color, #1
                        bcolors.ENDC, #2
                        bcolors.HEADER,#3
                        bcolors.UNDERLINE) #4
        return header
            
    def build_rows(self,buffer):
        rows=[]
        index=0
        
        for line in buffer:
            columns="{0}|{1}".format(bcolors.OKBLUE,bcolors.ENDC)
            print "E"
            print line
            if self.data_type.DATA == line['type']:
                for c in line['data']:
                    print c
                    if len('{}'.format(c))>self.column_character_width-2:
                        wall_color=bcolors.WARNING
                    else:
                        wall_color=bcolors.OKBLUE
                    columns+="{0}{1}|{2}".format(self.format_string(c,self.column_character_width,no_clip=self.no_clip),wall_color,bcolors.ENDC)
                if len(line['data']) < self.column_count:
                    wall_color=bcolors.OKBLUE
                    for c in range(len(line['data']),self.column_count):
                        columns+="{0}{1}|{2}".format(self.format_string("",self.column_character_width,no_clip=self.no_clip),wall_color,bcolors.ENDC)
            
            if self.data_type.COMMENT ==  line['type'] or self.data_type.WHITESPACE==line['type']:
                wall_color=bcolors.OKGREEN
                columns="{1}|{2}{0}{1}|{2}".format(self.format_string(line['raw'],self.total_width,no_clip=self.no_clip),wall_color,bcolors.OKGREEN)
                
            if self.data_type.ERROR ==  line['type']:
                wall_color=bcolors.OKGREEN
                columns="{1}|{2}{0}{1}|{2}".format(self.format_string(line['raw'],self.total_width,no_clip=self.no_clip),wall_color,bcolors.WARNING)
            rows.append(columns)
            index+=1
            #if index== int(tty_rows)-5:
            #    index=0
            #    rows.append(self.)
        return rows

            
    # with no columns, everything will be run on, not well formated
    def format(self):

        #here we either pull data from a file or read it from stdio as a if someone is  "cat something|ft"
        #if its a pipe, lets shove it into a temp file
        if select.select([sys.stdin,],[],[],0.0)[0]:
            fd, temp_path = tempfile.mkstemp()
            line=sys.stdin.read()
            os.write(fd,line)
            os.close(fd)
            self.file=temp_path
            self.is_temp_file=True

        else:
            if None == self.args.file:
                raise Exception("No input file available" )
            self.file=self.args.file
            if False == os.path.exists(self.file):
                raise Exception("file does not exist" )
            if False == os.path.isfile(self.file):
                raise Exception("not a valid file")


        # now we have a file, from stdin or a file on the system that we can access    
        buffer=self.process_file()
        print buffer
        
        #print(buffer)
        header=self.build_header()
        rows=self.build_rows(buffer)
        
        
        print (header)
        for row in rows:
            print (row)
        print (header)


    
        #print ("Error Count: {0}. Results: {1}".format(table.error_count(),table.results_length()) )
    
    def print_errors(table):
        for e in table.errors:
            print(e)