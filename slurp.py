#! /usr/bin/python -B
# -*- coding: utf-8 -*-

'''
Just a small app that download every comic from disneycomics.free.fr
and put them right where you are in a disney folder well organized.
'''

# Author:     Maxime Hadjinlian
#             maxime.hadjinlian@gmail.com
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import urllib2
import sys
import os
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    print 'You must install BeautifulSoup to use this app :'
    print '\t- via Crummy : http://www.crummy.com/software/BeautifulSoup/'
    print '\t- via Pypi : sudo easy_install beautifulsoup'
    sys.exit(1)

def fat32_valid(path):
    '''
    Take a path and clean it
    to be fat32 compatible.
    Replace all invalid char by _
    return the modified path
    '''
    invalid_char = ['"', '*', ':', \
                    '<', '>', '?', \
                    '|', ]
    for invalid in invalid_char:
        path = path.replace(invalid, '_')
    return path

def main():
    '''
    A main at least, we're not savages !
    '''

    import optparse

    usage = "Usage: %prog [options]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-d", "--dest", dest="dest", action="store",
                      default=os.getcwd(), 
                      help="Directory where to dump the comics.")

    options, _ = parser.parse_args()
    if (options.dest is None ) :
        dest = os.getcwd()
    else:
        if os.path.exists(options.dest):
            if os.path.isdir(options.dest):
                dest = options.dest
        else:
            print 'The destination : ' + options.dest,
            print ' does not exists or is not a folder.'
            sys.exit(1)

    authors = [ \
                ('Carl Barks', 'index_barks_date.php'), \
                ('Don Rosa', 'index_rosa_date.php'), \
                ('Marco Rota', 'index_rota_date.php'), \
                ('Romano Scarpa', 'index_scarpa_date.php'), \
                ('Tony Strobl', 'index_strobl_date.php'), \
                ('Vicar', 'index_vicar_date.php'), \
                ('William Van Horn', 'index_vanhorn_date.php'), \
                ('Paul Murry', 'index_murry_date.php'), \
                ('Sunday Strips', 'index_sunday.php'), \
                ('Daily Strips', 'index_dailies.php'), \
              ]

    different_struc = ['Paul Murry', 'Sunday Strips', 'Daily Strips']
    top_url = 'http://disneycomics.free.fr/'

    for author in authors:
        html = urllib2.urlopen(top_url + author[1])
        data = html.read()
        html.close()

        soup = BeautifulSoup(''.join(data))
        main_table = soup.table

        count = 0
        for comic in main_table.findAll('tr'):
            if count != 0:
                print
                if author[0] not in different_struc:
                    print 'Author : ' + author[0]
                    id_comic = str(''.join(comic.contents[1].\
                                   findAll(text=True)))
                    print 'Comics number :' + id_comic + ' (for this author)'
                    star = str(''.join(comic.contents[3].findAll(text=True)))
                    print "Star : " + star
                    inducks = str(comic.contents[5].find('a')['href'])
                    inducks = str(inducks.split('=')[2])
                    url = comic.contents[5].find('a')['href'].split('/')
                    url = str(top_url + url[0] + '/' \
                              + url[1] + '/' + inducks + '/')
                    print "URL : " + url
                    title = str(comic.contents[5].findAll(text=True)[0])
                    print "Title : " + title
                    year = str(''.join(comic.contents[7].findAll(text=True)))
                    if len(year) > 4:
                        year = year[-4:]
                    print "Year : " + year
                    nb_page = int(''.join(comic.contents[9].findAll(text=True)))
                    print "Nb Page : " + str(nb_page)
                    base_path = os.path.join('Disney', author[0], star, \
                                              year, title)
                    #Just replace invalid char in the filename for win32
                    if sys.platform == "win32" :
                        base_path = fat32_valid(base_path)
                    comic_path = os.path.join(dest, base_path)

                else:
                    # Paul Murry's page is different :/
                    print 'Author : ' + author[0]
                    id_comic = str(''.join(comic.contents[1].\
                                   findAll(text=True)))
                    print 'Comics number :' + id_comic + ' (for this author)'
                    inducks = str(comic.contents[5].find('a')['href'])
                    try:
                        inducks = str(inducks.split('=')[2])
                        url = comic.contents[3].find('a')['href'].split('/')
                        url = str(top_url + url[0] + '/' \
                                  + url[1] + '/' + inducks + '/')
                    except IndexError:
                        #case for daily and sunday
                        inducks = str(inducks.split('=')[1])
                        url = comic.contents[3].find('a')['href'].split('/')
                        url = str(top_url + url[0] + '/' + inducks + '/')

                    print "URL : " + url
                    title = str(comic.contents[3].findAll(text=True)[0])
                    print "Title : " + title
                    year = str(''.join(comic.contents[5].findAll(text=True)))
                    if author[0] in different_struc[1:]:
                        year = year.split('/')
                        year = year[len(year)-1]
                    elif len(year) > 4:
                        year = year[-4:]
                    print "Year : " + year
                    nb_page = int(''.join(comic.contents[7].\
                                  findAll(text=True)))
                    print "Nb Page : " + str(nb_page)
                    base_path = os.path.join('Disney', author[0], \
                                              'Mickey Mouse', year, title)
                    #Just replace invalid char in the filename for win32
                    if sys.platform == "win32" :
                        base_path = fat32_valid(base_path)
                    comic_path = os.path.join(dest, base_path)

                # Create folder structure
                if not os.path.exists(comic_path):
                    os.makedirs(comic_path)

                # Get the dir with the images
                html = urllib2.urlopen(url)
                data = html.read()
                html.close()

                soup = BeautifulSoup(''.join(data))
                count_img = 0
                sys.stdout.write("Done : 0/%d pages  \r" % (nb_page) )
                sys.stdout.flush()
                comic_advance = 0
                for img in soup.contents[2].findAll('a'):
                    if count_img > 4:
                        sys.stdout.write("Done : %d/%d pages  \r" \
                                         % (comic_advance, nb_page) )
                        sys.stdout.flush()
                        comic_file = urllib2.urlopen(url + img['href'])
                        comic_file_path = os.path.join(comic_path, img['href'])
                        output = open(comic_file_path, 'wb')
                        output.write(comic_file.read())
                        output.close()
                        comic_advance += 1
                        if comic_advance == nb_page:
                            sys.stdout.write("Done : %d/%d pages  \r" \
                                             % (comic_advance, nb_page) )
                            sys.stdout.flush()
                            print
                    else:
                        count_img += 1
            else:
                count += 1

if __name__ == '__main__' :
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
