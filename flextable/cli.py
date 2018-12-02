import argparse
from table import table

# table takes the data a s a file stream

            


def cli_main():
    parser = argparse.ArgumentParser("flextable", usage='%(prog)s [options]'
                    ,description=
                    """ascii table formatting with flexible columns, and styling
                    """, epilog="And that's how you flextable")

                                               
    # data
    parser.add_argument('-f'      ,'--file'                 , help='The input file to read')
    parser.add_argument('-c'      ,'--columns'              , help='column names')
    parser.add_argument('-cc'     ,'--column-count'         , help='column count, auto name columns 1-n'                ,default=-1, type=int)
    parser.add_argument('-cir'    ,'--header-on-line'       , help='column names the specified line of input'           ,default=-1, type=int,)
    parser.add_argument('-rq'     ,'--remove-quote'         , help='unwrap fields with block quotes'                    ,default=True)
    parser.add_argument('-bq'     ,'--block-quote'          , help='field block quote identifier'                       ,default=None)
    parser.add_argument('-ds'     ,'--data-on-line'         , help='data starts on this line'                           ,default=1,  type=int)
    
    # table template 
    parser.add_argument('-ln'     ,'--line-numbers'         , help='show line numbers'                                  ,action='store_true', default=False)
    parser.add_argument('-bs'     ,'--border-style'         , help='change table style, user definable'                 ,default='default_style.yml')
    parser.add_argument('-ft'     ,'--footer'               , help='show the footer'                                    ,action='store_true', default=True)
    parser.add_argument('-ftc'    ,'--footer-columns'       , help='footer has column names'                            ,action='store_true', default=True)
    parser.add_argument('-ls'     ,'--line-seperators'      , help='use line seperators for each column of data'        ,action='store_true', default=False)
    
    # formatting 
    parser.add_argument('-e'      ,'--error'                , help='rows with invalid number of columns are considered errors', action='store_true', default=True)
    parser.add_argument('-cm'     ,'--comment'              , help='character that denotes line is comment, \'#\' default'    , default="#")
    parser.add_argument('-d'      ,'--delimiter'            , help='field delimiter \',\' default'                      ,default=",")
    
    # display
    parser.add_argument('-he'      ,'--hide-errors'         , help='do not display errors'                              ,action='store_true' ,default=False)
    parser.add_argument('-hc'      ,'--hide-comments'       , help='do not display comments'                            ,action='store_true' ,default=False)
    parser.add_argument('-hw'      ,'--hide-whitespace'     , help='do not display whitespace'                          ,action='store_true' ,default=False)

    # limit,pagination
    parser.add_argument('-l'      ,'--line'                 , help='line number to start displaying data from in file'  ,type=int,default=-1)
    parser.add_argument('-len'    ,'--length'               , help='number of lines to show, hidden lines do not count' ,type=int,default=-1)
    parser.add_argument('-p'      ,'--page'                 , help='page to start displaying, requires length parameter',type=int,default=-1)
 
    # output
    parser.add_argument('-y'      ,'--yaml'                 , help='output yaml')
    parser.add_argument('-j'      ,'--json'                 , help='output json')

    args=parser.parse_args()

    table(args)


if __name__ == "__main__":
    cli_main()