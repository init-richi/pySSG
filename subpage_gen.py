###################################
# author: Richard Mietz           #
# ver: 1.0                        #
# date: 23.08.2016                #
# subpage_gen.py : builds subpages#
# Copyright 2016 Richard Mietz    #
###################################
#    This file is part of pySSG.
#
#    pySSG is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    pySSG is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pySSG.  If not, see <http://www.gnu.org/licenses/>.
#
#    Diese Datei ist Teil von pySSG.
#
#    pySSG ist Freie Software: Sie können es unter den Bedingungen
#    der GNU General Public License, wie von der Free Software Foundation,
#    Version 3 der Lizenz oder (nach Ihrer Wahl) jeder späteren
#    veröffentlichten Version, weiterverbreiten und/oder modifizieren.
#
#    pySSG wird in der Hoffnung, dass es nützlich sein wird, aber
#    OHNE JEDE GEWÄHRLEISTUNG, bereitgestellt; sogar ohne die implizite
#    Gewährleistung der MARKTFÄHIGKEIT oder EIGNUNG FÜR EINEN BESTIMMTEN ZWECK.
#    Siehe die GNU General Public License für weitere Details.
#
#    Sie sollten eine Kopie der GNU General Public License zusammen mit diesem
#    Programm erhalten haben. Wenn nicht, siehe <http://www.gnu.org/licenses/>.

import os, fileinput

print('writing main_navigation to subpages...')
print('building and writing sub navigation to subpages')
folder = os.listdir('web')
for files in folder:
    if files.endswith('.html') | files.endswith('.php'):
        file = open('content/'+files, 'r').readlines()
        header = file[1:4]
        sidebar = header[2]
        sidebar = sidebar[8:-1]
        if sidebar[0:4] == 'nav.':
            file = open('tmp/nav_'+sidebar[4:]+'.temp', 'w').write('<ul>\n')
            sub_folder = os.listdir('content/subpages')
            for sub_files in sub_folder:
                if sub_files.endswith(sidebar[4:0]+'.html') | sub_files.endswith(sidebar[4:0]+'.php'):
                    file = open('content/subpages/'+sub_files, 'r').readlines()
                    header = file[1:4]
                    navname = header[1]
                    navname = navname[8:-1]
                    file = open('tmp/nav_' + sidebar[4:] + '.temp', 'a')
                    file.write(' <li><a href="subpages/'+sub_files+'">'+navname+'</a></li>\n')
            file = open('tmp/nav_' + sidebar[4:] + '.temp', 'a')
            file.write('</ul>')
            file.close()
            filetmp = open('tmp/nav_' + sidebar[4:] + '.temp', 'r').read()
            with fileinput.FileInput('web/'+files, inplace=True) as file:
                for line in file:
                    print(line.replace('{sidebar}', filetmp), end="")
            for sub_files in sub_folder:
                if sub_files.endswith(sidebar[4:]+'.html') | sub_files.endswith(sidebar[4:0]+'.php'):
                    with fileinput.FileInput('web/subpages/'+sub_files, inplace=True) as file:
                        for line in file:
                            print(line.replace('{sidebar}', filetmp), end="")
                    with fileinput.FileInput('web/subpages/'+sub_files, inplace=True) as file:
                        for line in file:
                            print(line.replace('{navigation}', open('tmp/nav.temp').read()), end="")

print('done\n\n')
print('finishing subpages...')
folder_sub = os.listdir('web/subpages')
for files in folder_sub:
    if files.endswith('.html') | files.endswith('.php'):
        with fileinput.FileInput('web/subpages/' + files, inplace=True) as file:
            for line in file:
                print(line.replace('subpages/', ''), end="")
        with fileinput.FileInput('web/subpages/' + files, inplace=True) as file:
            for line in file:
                print(line.replace('stylesheet/', '../stylesheet/'), end="")
        with fileinput.FileInput('web/subpages/' + files, inplace=True) as file:
            for line in file:
                print(line.replace('files/', '../files/'), end="")

cfile_folder = os.listdir('content/subpages')
for cfile in cfile_folder:
    if cfile.endswith('.html') | cfile.endswith('.php'):
        wfile = cfile
        file = open('content/subpages/' + cfile, 'r').readlines()
        title = file[1]
        title = title[6:-1]
        content = file[5:]
        content = ''.join(str(i) for i in content)
        with fileinput.FileInput('web/subpages/' + wfile, inplace=True) as file:
            for line in file:
                print(line.replace('{content}', content), end="")
        with fileinput.FileInput('web/subpages/' + wfile, inplace=True) as file:
            for line in file:
                print(line.replace('{title}', title), end="")
print('done\n\n')
os.system('rm tmp/*')
